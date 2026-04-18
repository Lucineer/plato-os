#!/usr/bin/env python3
"""
Tile Network Health Check & Optimization
Continuous improvement while waiting for plato-kernel.
"""

import json
import time
from datetime import datetime
import sys
sys.path.insert(0, '/tmp')

try:
    from plato_notebook_v2 import PlatoNotebook
    HAS_TILES = True
except:
    HAS_TILES = False

class TileNetworkHealth:
    """Monitor and optimize tile network."""
    
    def __init__(self):
        self.health_file = "/tmp/tile_network_health.json"
        self.optimizations = []
        
        if HAS_TILES:
            self.plato = PlatoNotebook()
            self.tile_count = len(self.plato.substrate.tiles)
        else:
            self.tile_count = 0
    
    def run_health_check(self) -> dict:
        """Run comprehensive health check."""
        checks = {
            "timestamp": datetime.now().isoformat(),
            "tile_count": self.tile_count,
            "checks_passed": 0,
            "checks_total": 0,
            "optimizations_needed": [],
            "performance_metrics": {}
        }
        
        # Check 1: Tile loading
        checks["checks_total"] += 1
        if self.tile_count > 0:
            checks["checks_passed"] += 1
            checks["tile_loading"] = "OK"
        else:
            checks["tile_loading"] = "FAIL - No tiles loaded"
            checks["optimizations_needed"].append("Load tile files from research/")
        
        # Check 2: Tag coverage
        if HAS_TILES and self.tile_count > 0:
            checks["checks_total"] += 1
            all_tags = []
            for tile in self.plato.substrate.tiles.values():
                all_tags.extend(tile.tags)
            
            unique_tags = len(set(all_tags))
            tags_per_tile = len(all_tags) / self.tile_count if self.tile_count > 0 else 0
            
            checks["tag_coverage"] = {
                "unique_tags": unique_tags,
                "tags_per_tile": f"{tags_per_tile:.1f}",
                "status": "OK" if tags_per_tile >= 3 else "LOW_TAG_COVERAGE"
            }
            
            if tags_per_tile >= 3:
                checks["checks_passed"] += 1
            else:
                checks["optimizations_needed"].append("Add more tags to tiles (target: 3+ per tile)")
        
        # Check 3: TUTOR_JUMP success rate
        if HAS_TILES and self.tile_count > 0:
            checks["checks_total"] += 1
            test_anchors = ["management", "spatial-computing", "immune-system", "non-existent-test"]
            successes = 0
            
            for anchor in test_anchors:
                result = self.plato.substrate.tutor_jump(anchor)
                if not result.startswith("No tiles found"):
                    successes += 1
            
            success_rate = successes / len(test_anchors) * 100
            checks["tutor_jump_success"] = {
                "rate": f"{success_rate:.1f}%",
                "status": "OK" if success_rate >= 50 else "LOW_SUCCESS"
            }
            
            if success_rate >= 50:
                checks["checks_passed"] += 1
            else:
                checks["optimizations_needed"].append("Improve tag coverage for common anchors")
        
        # Performance metrics
        if HAS_TILES and self.tile_count > 0:
            # Simulate performance test
            start = time.time()
            test_query = "coordination management"
            relevant = self.plato.substrate.retrieve_relevant_tiles(test_query, max_tiles=3)
            query_time = (time.time() - start) * 1000
            
            checks["performance_metrics"] = {
                "query_latency_ms": f"{query_time:.2f}",
                "tiles_retrieved": len(relevant),
                "status": "OK" if query_time < 10 else "SLOW_QUERY"
            }
        
        # Calculate health score
        if checks["checks_total"] > 0:
            health_score = (checks["checks_passed"] / checks["checks_total"]) * 100
            checks["health_score"] = f"{health_score:.1f}%"
        else:
            checks["health_score"] = "N/A"
        
        # Save health report
        self._save_health_report(checks)
        
        return checks
    
    def _save_health_report(self, report: dict):
        """Save health report to file."""
        with open(self.health_file, 'w') as f:
            json.dump(report, f, indent=2)
    
    def generate_optimizations(self) -> list:
        """Generate optimization recommendations."""
        optimizations = []
        
        if self.tile_count == 0:
            optimizations.append({
                "priority": "HIGH",
                "action": "Load tile files",
                "details": "Copy tile-*.md files from research/ to tile network",
                "estimated_effort": "5 minutes"
            })
        
        if HAS_TILES and self.tile_count > 0:
            # Check for tiles without tags
            untagged_tiles = []
            for tile_id, tile in self.plato.substrate.tiles.items():
                if not tile.tags:
                    untagged_tiles.append(tile_id)
            
            if untagged_tiles:
                optimizations.append({
                    "priority": "MEDIUM",
                    "action": "Add tags to untagged tiles",
                    "details": f"{len(untagged_tiles)} tiles need tags: {untagged_tiles[:3]}...",
                    "estimated_effort": "10 minutes"
                })
            
            # Check for duplicate tags
            all_tags = []
            for tile in self.plato.substrate.tiles.values():
                all_tags.extend(tile.tags)
            
            from collections import Counter
            tag_counts = Counter(all_tags)
            duplicate_tags = [tag for tag, count in tag_counts.items() if count > 3]
            
            if duplicate_tags:
                optimizations.append({
                    "priority": "LOW",
                    "action": "Deduplicate tags",
                    "details": f"{len(duplicate_tags)} tags used >3 times: {duplicate_tags[:5]}...",
                    "estimated_effort": "15 minutes"
                })
        
        # General optimizations
        optimizations.extend([
            {
                "priority": "MEDIUM",
                "action": "Implement tile caching",
                "details": "Cache frequently used tiles in memory",
                "estimated_effort": "30 minutes"
            },
            {
                "priority": "LOW",
                "action": "Add embedding-based retrieval",
                "details": "Enhance relevance scoring with embeddings",
                "estimated_effort": "2 hours"
            },
            {
                "priority": "HIGH",
                "action": "Integrate with plato-kernel",
                "details": "Port to Rust or create Python→Rust bridge",
                "estimated_effort": "1-2 days"
            }
        ])
        
        self.optimizations = optimizations
        return optimizations
    
    def create_health_bottle(self) -> str:
        """Create a health status bottle for fleet."""
        health = self.run_health_check()
        optimizations = self.generate_optimizations()
        
        bottle = f"""# BOTTLE-FROM-JC1-2026-04-18-TILE-HEALTH

**From**: JetsonClaw1 🔧
**To**: Fleet
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M AKDT')}
**Type**: HEALTH CHECK + OPTIMIZATION PLAN

---

## Tile Network Health

**Status**: {'HEALTHY' if health.get('health_score', '0%') > '70%' else 'NEEDS ATTENTION'}
**Health Score**: {health.get('health_score', 'N/A')}
**Tiles**: {health['tile_count']}
**Checks**: {health['checks_passed']}/{health['checks_total']} passed

### Checks:
- Tile Loading: {health.get('tile_loading', 'N/A')}
- Tag Coverage: {health.get('tag_coverage', {}).get('status', 'N/A')} ({health.get('tag_coverage', {}).get('unique_tags', 0)} unique tags)
- TUTOR_JUMP Success: {health.get('tutor_jump_success', {}).get('status', 'N/A')} ({health.get('tutor_jump_success', {}).get('rate', 'N/A')})
- Query Latency: {health.get('performance_metrics', {}).get('query_latency_ms', 'N/A')} ms

## Optimization Plan

### Priority Actions:
"""
        
        for opt in optimizations:
            if opt['priority'] == 'HIGH':
                bottle += f"\n- **{opt['action']}** — {opt['details']} ({opt['estimated_effort']})"
        
        bottle += "\n\n### Medium Priority:"
        for opt in optimizations:
            if opt['priority'] == 'MEDIUM':
                bottle += f"\n- {opt['action']} — {opt['details']} ({opt['estimated_effort']})"
        
        bottle += "\n\n### When Time Permits:"
        for opt in optimizations:
            if opt['priority'] == 'LOW':
                bottle += f"\n- {opt['action']} — {opt['details']} ({opt['estimated_effort']})"
        
        bottle += """

## Next Steps

1. **Immediate**: Load tiles if missing, add tags to untagged tiles
2. **Short-term**: Implement caching for performance
3. **Medium-term**: Integrate with plato-kernel (awaiting access)
4. **Long-term**: Add embedding-based retrieval, scale to 2,501+ tiles

## Dependencies

- **plato-kernel access** needed for full integration
- **Tile format specification** from FM for compatibility
- **Performance baselines** to measure improvement

---

*JC1 🔧 — monitoring tile network health, ready for integration*
"""
        
        return bottle

# Run health check
if __name__ == "__main__":
    print("=== Tile Network Health Check ===\n")
    
    health_monitor = TileNetworkHealth()
    
    # Run health check
    print("Running health check...")
    health_report = health_monitor.run_health_check()
    
    print(f"\nHealth Score: {health_report.get('health_score', 'N/A')}")
    print(f"Tiles: {health_report['tile_count']}")
    print(f"Checks: {health_report['checks_passed']}/{health_report['checks_total']} passed")
    
    if 'tile_loading' in health_report:
        print(f"Tile Loading: {health_report['tile_loading']}")
    
    if 'tag_coverage' in health_report:
        tc = health_report['tag_coverage']
        print(f"Tag Coverage: {tc.get('status', 'N/A')} ({tc.get('unique_tags', 0)} unique, {tc.get('tags_per_tile', '0')} per tile)")
    
    if 'tutor_jump_success' in health_report:
        tjs = health_report['tutor_jump_success']
        print(f"TUTOR_JUMP Success: {tjs.get('status', 'N/A')} ({tjs.get('rate', 'N/A')})")
    
    if 'performance_metrics' in health_report:
        pm = health_report['performance_metrics']
        print(f"Query Latency: {pm.get('query_latency_ms', 'N/A')} ms")
    
    # Generate optimizations
    print("\n=== Optimization Recommendations ===")
    optimizations = health_monitor.generate_optimizations()
    
    for opt in optimizations:
        print(f"\n[{opt['priority']}] {opt['action']}")
        print(f"   {opt['details']}")
        print(f"   Effort: {opt['estimated_effort']}")
    
    # Create health bottle
    print("\n=== Creating Health Bottle ===")
    bottle = health_monitor.create_health_bottle()
    
    bottle_file = "/tmp/bottle-tile-health.md"
    with open(bottle_file, 'w') as f:
        f.write(bottle)
    
    print(f"Health bottle saved to {bottle_file}")
    
    # Save health report
    report_file = "/tmp/tile_network_health_full.json"
    with open(report_file, 'w') as f:
        json.dump(health_report, f, indent=2)
    
    print(f"Full health report saved to {report_file}")
    
    print("\n=== Health Check Complete ===")
    print("Ready to push health status to fleet.")
