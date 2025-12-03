"""
Community Reviews API endpoints
Part of ENH-007: Review Visualization & Social Features
"""

from flask import request, jsonify
from flask_login import login_required, current_user
from app.api import bp
from app.models import BeverageReview, Bottle, db
from sqlalchemy import func, desc
from datetime import datetime


@bp.route('/reviews', methods=['GET'])
@login_required
def get_reviews():
    """Get community reviews for a beverage."""
    
    beverage_name = request.args.get('beverage_name', '').strip()
    beverage_brand = request.args.get('beverage_brand', '').strip()
    limit = int(request.args.get('limit', 20))
    offset = int(request.args.get('offset', 0))
    
    query = BeverageReview.query.filter_by(is_public=True)
    
    if beverage_name:
        query = query.filter_by(beverage_name=beverage_name)
    
    if beverage_brand:
        query = query.filter_by(beverage_brand=beverage_brand)
    
    # Order by most recent
    reviews = query.order_by(desc(BeverageReview.created_at)).offset(offset).limit(limit).all()
    total = query.count()
    
    return jsonify({
        'reviews': [r.to_dict(include_user=True) for r in reviews],
        'total': total,
        'limit': limit,
        'offset': offset
    })


@bp.route('/reviews/stats/<beverage_name>', methods=['GET'])
@login_required
def get_review_stats(beverage_name):
    """Get aggregated review statistics for a beverage."""
    
    brand = request.args.get('brand', '').strip()
    
    query = BeverageReview.query.filter_by(
        beverage_name=beverage_name,
        is_public=True
    )
    
    if brand:
        query = query.filter_by(beverage_brand=brand)
    
    # Aggregate statistics
    total_reviews = query.count()
    
    if total_reviews == 0:
        return jsonify({
            'beverage_name': beverage_name,
            'beverage_brand': brand,
            'total_reviews': 0,
            'average_rating': None,
            'rating_distribution': {}
        })
    
    # Calculate average rating
    avg_rating = query.with_entities(func.avg(BeverageReview.rating)).scalar()
    
    # Rating distribution
    rating_dist = {}
    for rating_val in range(11):  # 0-10
        count = query.filter_by(rating=float(rating_val)).count()
        if count > 0:
            rating_dist[str(rating_val)] = count
    
    return jsonify({
        'beverage_name': beverage_name,
        'beverage_brand': brand,
        'total_reviews': total_reviews,
        'average_rating': round(avg_rating, 2) if avg_rating else None,
        'rating_distribution': rating_dist
    })


@bp.route('/reviews', methods=['POST'])
@login_required
def create_review():
    """Create a new community review."""
    
    data = request.get_json() or {}
    
    beverage_name = data.get('beverage_name', '').strip()
    if not beverage_name:
        return jsonify({'error': 'Beverage name is required'}), 400
    
    rating = data.get('rating')
    if rating is None:
        return jsonify({'error': 'Rating is required'}), 400
    
    try:
        rating = float(rating)
        if rating < 0 or rating > 10:
            return jsonify({'error': 'Rating must be between 0 and 10'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid rating value'}), 400
    
    # Check if user already reviewed this beverage
    existing = BeverageReview.query.filter_by(
        beverage_name=beverage_name,
        beverage_brand=data.get('beverage_brand', '').strip() or None,
        user_id=current_user.id
    ).first()
    
    if existing:
        # Update existing review
        existing.rating = rating
        existing.review_text = data.get('review_text', '').strip()
        existing.is_public = data.get('is_public', True)
        existing.is_anonymous = data.get('is_anonymous', True)
        existing.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(existing.to_dict()), 200
    
    # Create new review
    review = BeverageReview(
        beverage_name=beverage_name,
        beverage_brand=data.get('beverage_brand', '').strip() or None,
        user_id=current_user.id,
        rating=rating,
        review_text=data.get('review_text', '').strip(),
        is_public=data.get('is_public', True),
        is_anonymous=data.get('is_anonymous', True)
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify(review.to_dict()), 201


@bp.route('/reviews/popular', methods=['GET'])
@login_required
def get_popular_beverages():
    """Get most popular beverages based on review counts and ratings."""
    
    category = request.args.get('category', '').strip()
    limit = int(request.args.get('limit', 10))
    
    # Get beverages with most reviews and highest average ratings
    query = db.session.query(
        BeverageReview.beverage_name,
        BeverageReview.beverage_brand,
        func.count(BeverageReview.id).label('review_count'),
        func.avg(BeverageReview.rating).label('avg_rating')
    ).filter(
        BeverageReview.is_public == True
    ).group_by(
        BeverageReview.beverage_name,
        BeverageReview.beverage_brand
    ).having(
        func.count(BeverageReview.id) >= 3  # At least 3 reviews
    ).order_by(
        desc('avg_rating'),
        desc('review_count')
    ).limit(limit)
    
    results = []
    for name, brand, count, avg in query.all():
        results.append({
            'beverage_name': name,
            'beverage_brand': brand,
            'review_count': count,
            'average_rating': round(avg, 2)
        })
    
    return jsonify({
        'beverages': results,
        'limit': limit
    })


@bp.route('/reviews/compare', methods=['GET'])
@login_required
def compare_ratings():
    """Compare user's ratings with community averages."""
    
    # Get user's rated bottles
    user_bottles = Bottle.query.filter_by(
        user_id=current_user.id,
        tasted=True
    ).filter(Bottle.rating.isnot(None)).all()
    
    comparisons = []
    for bottle in user_bottles:
        # Get community stats for this beverage
        community_stats = db.session.query(
            func.avg(BeverageReview.rating).label('avg_rating'),
            func.count(BeverageReview.id).label('review_count')
        ).filter_by(
            beverage_name=bottle.name,
            beverage_brand=bottle.category,  # Using category as proxy for brand if needed
            is_public=True
        ).first()
        
        if community_stats and community_stats.review_count > 0:
            comparisons.append({
                'beverage_name': bottle.name,
                'user_rating': bottle.rating,
                'community_average': round(community_stats.avg_rating, 2),
                'community_review_count': community_stats.review_count,
                'difference': round((bottle.rating or 0) - community_stats.avg_rating, 2)
            })
    
    return jsonify({
        'comparisons': comparisons,
        'total': len(comparisons)
    })

