"""
Whisky Database Integration Module
Handles integration with various whisky data sources and APIs
"""

import requests
import json
import time
from datetime import datetime, timedelta
from app.api import bp
from app.models import MasterBeverage, db
from flask_login import login_required
from flask import request, jsonify, current_app
from werkzeug.exceptions import BadRequest
import logging

logger = logging.getLogger(__name__)

class WhiskyDataSource:
    """Base class for whisky data sources"""

    def __init__(self, name, base_url, api_key=None):
        self.name = name
        self.base_url = base_url
        self.api_key = api_key
        self.last_request = None
        self.rate_limit_delay = 1  # seconds between requests

    def _rate_limit(self):
        """Implement rate limiting"""
        if self.last_request:
            elapsed = (datetime.now() - self.last_request).total_seconds()
            if elapsed < self.rate_limit_delay:
                time.sleep(self.rate_limit_delay - elapsed)
        self.last_request = datetime.now()

    def search(self, query, limit=50):
        """Search for whiskies - to be implemented by subclasses"""
        raise NotImplementedError

    def get_whisky(self, whisky_id):
        """Get detailed whisky information - to be implemented by subclasses"""
        raise NotImplementedError

    def normalize_whisky_data(self, raw_data):
        """Normalize whisky data to our standard format"""
        return {
            'external_id': raw_data.get('id'),
            'name': raw_data.get('name', '').strip(),
            'brand': raw_data.get('distillery', raw_data.get('brand', '')).strip(),
            'category': self._determine_category(raw_data),
            'abv': float(raw_data.get('abv', 0)) if raw_data.get('abv') else None,
            'region': raw_data.get('region', '').strip(),
            'country': raw_data.get('country', '').strip(),
            'description': raw_data.get('description', '').strip(),
            'tasting_notes': raw_data.get('tasting_notes', '').strip(),
            'image_url': raw_data.get('image_url', '').strip(),
            'source': self.name,
            'verified': False  # External data needs verification
        }

    def _determine_category(self, data):
        """Determine whisky category from data"""
        # This is a basic implementation - can be enhanced
        whisky_type = data.get('type', '').lower()
        if 'single malt' in whisky_type:
            return 'scotch'
        elif 'bourbon' in whisky_type:
            return 'bourbon'
        elif 'irish' in whisky_type:
            return 'irish'
        elif 'rye' in whisky_type:
            return 'bourbon'  # rye is a type of bourbon
        else:
            return 'scotch'  # default


class WhiskybaseSource(WhiskyDataSource):
    """Integration with Whiskybase"""

    def __init__(self):
        super().__init__('whiskybase', 'https://www.whiskybase.com')
        # Whiskybase may not have a public API - this is placeholder
        self.has_api = False

    def search(self, query, limit=50):
        """Whiskybase search - placeholder for future API or scraping"""
        logger.info(f"Whiskybase search not implemented yet: {query}")
        return []

    def get_whisky(self, whisky_id):
        """Get whisky details - placeholder"""
        logger.info(f"Whiskybase get_whisky not implemented: {whisky_id}")
        return None


class DistillerSource(WhiskyDataSource):
    """Integration with Distiller"""

    def __init__(self):
        super().__init__('distiller', 'https://distiller.com')
        # Distiller may not have a public API
        self.has_api = False

    def search(self, query, limit=50):
        """Distiller search - placeholder"""
        logger.info(f"Distiller search not implemented yet: {query}")
        return []

    def get_whisky(self, whisky_id):
        """Get whisky details - placeholder"""
        logger.info(f"Distiller get_whisky not implemented: {whisky_id}")
        return None


class MasterOfMaltSource(WhiskyDataSource):
    """Integration with Master of Malt"""

    def __init__(self):
        super().__init__('masterofmalt', 'https://www.masterofmalt.com')
        # Master of Malt may not have a public API
        self.has_api = False

    def search(self, query, limit=50):
        """Master of Malt search - placeholder"""
        logger.info(f"Master of Malt search not implemented yet: {query}")
        return []

    def get_whisky(self, whisky_id):
        """Get whisky details - placeholder"""
        logger.info(f"Master of Malt get_whisky not implemented: {whisky_id}")
        return None


class SampleWhiskyDataSource(WhiskyDataSource):
    """Sample whisky data for testing and demonstration"""

    def __init__(self):
        super().__init__('sample', 'https://sample-whisky-db.example.com')
        self.has_api = True
        self.sample_data = self._load_sample_data()

    def _load_sample_data(self):
        """Load sample whisky data"""
        return [
            {
                'id': 'macallan-12',
                'name': 'Macallan 12 Year Old Sherry Oak',
                'distillery': 'Macallan',
                'type': 'single malt scotch',
                'abv': 43.0,
                'region': 'Speyside',
                'country': 'Scotland',
                'description': 'A rich and elegant single malt with notes of sherry, dried fruits, and oak.',
                'tasting_notes': 'Sherry sweetness with dark chocolate, orange peel, and a long finish.',
                'image_url': 'https://example.com/macallan-12.jpg'
            },
            {
                'id': 'glenfiddich-12',
                'name': 'Glenfiddich 12 Year Old',
                'distillery': 'Glenfiddich',
                'type': 'single malt scotch',
                'abv': 40.0,
                'region': 'Speyside',
                'country': 'Scotland',
                'description': 'Light and fresh with pear drops, apple, and a hint of oak.',
                'tasting_notes': 'Fresh green apples, pear, and subtle oak with a clean finish.',
                'image_url': 'https://example.com/glenfiddich-12.jpg'
            },
            {
                'id': 'lagavulin-16',
                'name': 'Lagavulin 16 Year Old',
                'distillery': 'Lagavulin',
                'type': 'single malt scotch',
                'abv': 43.0,
                'region': 'Islay',
                'country': 'Scotland',
                'description': 'Intensely peated with smoky, maritime character.',
                'tasting_notes': 'Peat smoke, sea salt, iodine, and dark chocolate.',
                'image_url': 'https://example.com/lagavulin-16.jpg'
            },
            {
                'id': 'buffalo-trace',
                'name': 'Buffalo Trace Kentucky Straight Bourbon',
                'distillery': 'Buffalo Trace',
                'type': 'bourbon',
                'abv': 45.0,
                'region': 'Kentucky',
                'country': 'USA',
                'description': 'Well-balanced bourbon with vanilla, caramel, and oak notes.',
                'tasting_notes': 'Rich vanilla, caramel, oak, with hints of spice.',
                'image_url': 'https://example.com/buffalo-trace.jpg'
            },
            {
                'id': 'jameson-irish',
                'name': 'Jameson Irish Whiskey',
                'distillery': 'Jameson',
                'type': 'irish whiskey',
                'abv': 40.0,
                'region': 'Dublin',
                'country': 'Ireland',
                'description': 'Triple distilled for smoothness with vanilla and spice.',
                'tasting_notes': 'Light and smooth with vanilla, spice, and a clean finish.',
                'image_url': 'https://example.com/jameson.jpg'
            }
        ]

    def search(self, query, limit=50):
        """Search sample whisky database"""
        query_lower = query.lower()
        results = []

        for whisky in self.sample_data:
            # Search in name, distillery, description
            searchable_text = f"{whisky['name']} {whisky.get('distillery', '')} {whisky.get('description', '')}".lower()
            if query_lower in searchable_text:
                results.append(self.normalize_whisky_data(whisky))

        return results[:limit]

    def get_whisky(self, whisky_id):
        """Get whisky details from sample data"""
        for whisky in self.sample_data:
            if whisky['id'] == whisky_id:
                return self.normalize_whisky_data(whisky)
        return None


class OpenWhiskyDataSource(WhiskyDataSource):
    """Integration with open whisky data sources"""

    def __init__(self):
        super().__init__('openwhisky', 'https://openwhisky.org')
        # Open Whisky project - may have API
        self.has_api = True

    def search(self, query, limit=50):
        """Search Open Whisky database"""
        try:
            self._rate_limit()
            # This is a placeholder - need to check actual API
            url = f"{self.base_url}/api/search"
            params = {'q': query, 'limit': limit}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            return [self.normalize_whisky_data(item) for item in data.get('results', [])]
        except Exception as e:
            logger.error(f"Open Whisky search error: {e}")
            return []

    def get_whisky(self, whisky_id):
        """Get whisky details from Open Whisky"""
        try:
            self._rate_limit()
            url = f"{self.base_url}/api/whisky/{whisky_id}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            return self.normalize_whisky_data(data)
        except Exception as e:
            logger.error(f"Open Whisky get_whisky error: {e}")
            return None


# Global registry of whisky data sources
WHISKY_SOURCES = {
    'sample': SampleWhiskyDataSource(),  # Sample data for testing
    'whiskybase': WhiskybaseSource(),    # Placeholder for future API
    'distiller': DistillerSource(),      # Placeholder for future API
    'masterofmalt': MasterOfMaltSource(), # Placeholder for future API
    'openwhisky': OpenWhiskyDataSource(), # Placeholder for future API
}


@bp.route('/whisky/search', methods=['GET'])
@login_required
def search_whisky_databases():
    """Search across all whisky databases"""

    logger.info("Whisky search request received")

    query = request.args.get('q', '').strip()
    sources = request.args.get('sources', 'all').split(',')
    limit = int(request.args.get('limit', 20))

    logger.info(f"Search parameters: query='{query}', sources={sources}, limit={limit}")

    if not query:
        logger.warning("Search query is empty")
        return jsonify({'error': 'Search query required'}), 400

    results = []
    source_results = {}

    # Search each requested source
    sources_to_search = ['sample'] if 'all' in sources else [s for s in sources if s in ['sample', 'whiskybase', 'distiller', 'masterofmalt']]
    logger.info(f"Sources to search: {list(sources_to_search)}")

    for source_name in sources_to_search:
        if source_name in WHISKY_SOURCES:
            source = WHISKY_SOURCES[source_name]
            try:
                logger.info(f"Searching source: {source_name}")
                source_results[source_name] = source.search(query, limit // len(sources_to_search))
                results.extend(source_results[source_name])
                logger.info(f"Source {source_name} returned {len(source_results[source_name])} results")
            except Exception as e:
                logger.error(f"Error searching {source_name}: {e}", exc_info=True)
                source_results[source_name] = []
        else:
            logger.warning(f"Unknown source requested: {source_name}")

    logger.info(f"Total results before sorting: {len(results)}")

    # Sort results by relevance (simple name matching for now)
    results.sort(key=lambda x: x['name'].lower().find(query.lower()), reverse=True)

    # Limit total results
    results = results[:limit]

    logger.info(f"Final results: {len(results)} items")

    response_data = {
        'query': query,
        'total_results': len(results),
        'sources_searched': list(sources_to_search),
        'source_results': source_results,
        'results': results
    }

    logger.info("Whisky search completed successfully")
    return jsonify(response_data)


@bp.route('/whisky/<source>/<whisky_id>', methods=['GET'])
@login_required
def get_whisky_details(source, whisky_id):
    """Get detailed whisky information from a specific source"""

    if source not in WHISKY_SOURCES:
        return jsonify({'error': 'Unknown whisky source'}), 400

    source_obj = WHISKY_SOURCES[source]
    whisky_data = source_obj.get_whisky(whisky_id)

    if not whisky_data:
        return jsonify({'error': 'Whisky not found'}), 404

    return jsonify(whisky_data)


@bp.route('/whisky/sources', methods=['GET'])
@login_required
def get_whisky_sources():
    """Get information about available whisky data sources"""

    sources_info = {}
    for name, source in WHISKY_SOURCES.items():
        sources_info[name] = {
            'name': source.name,
            'has_api': getattr(source, 'has_api', False),
            'base_url': source.base_url
        }

    return jsonify({
        'sources': sources_info
    })


@bp.route('/whisky/import', methods=['POST'])
@login_required
def import_whisky_to_catalog():
    """Import whisky from external source to master catalog"""

    data = request.get_json() or {}
    source = data.get('source')
    whisky_id = data.get('whisky_id')

    if not source or not whisky_id:
        return jsonify({'error': 'Source and whisky_id required'}), 400

    if source not in WHISKY_SOURCES:
        return jsonify({'error': 'Unknown whisky source'}), 400

    # Get whisky data from source
    source_obj = WHISKY_SOURCES[source]
    whisky_data = source_obj.get_whisky(whisky_id)

    if not whisky_data:
        return jsonify({'error': 'Whisky not found in source'}), 404

    # Check if already exists in catalog
    existing = MasterBeverage.query.filter_by(
        name=whisky_data['name'],
        brand=whisky_data.get('brand')
    ).first()

    if existing:
        return jsonify({
            'error': 'Whisky already exists in catalog',
            'existing_id': existing.id
        }), 409

    # Create new catalog entry
    beverage = MasterBeverage(
        name=whisky_data['name'],
        brand=whisky_data.get('brand'),
        category=whisky_data.get('category', 'other'),
        abv=whisky_data.get('abv'),
        region=whisky_data.get('region'),
        country=whisky_data.get('country'),
        description=whisky_data.get('description'),
        tasting_notes=whisky_data.get('tasting_notes'),
        image_url=whisky_data.get('image_url'),
        external_id=whisky_data.get('external_id'),
        source=whisky_data.get('source', source),
        verified=False  # Imported data needs verification
    )

    db.session.add(beverage)
    db.session.commit()

    return jsonify({
        'message': 'Whisky imported to catalog',
        'beverage': beverage.to_dict()
    }), 201
