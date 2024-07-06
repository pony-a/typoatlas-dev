<script setup lang="ts">
import 'maplibre-gl/dist/maplibre-gl.css';
import { Map, Popup, GeoJSONSource } from 'maplibre-gl';
import { onMounted } from 'vue';
import { long2tile, lat2tile, tile2bounds, tileXYToQuadKey } from '../tileUtils';

onMounted(() => {



    const map = new Map({
        container: 'map',
        style: {
            version: 8,
            sources: {
                pale: {
                    type: 'raster',
                    tiles: ['https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png'],
                    tileSize: 256,
                    attribution:
                        '地理院タイル',
                },
            },
            layers: [
                {
                    id: 'pale',
                    type: 'raster',
                    source: 'pale',
                    minzoom: 0,
                    maxzoom: 18,
                },
            ],
        },//地理院タイル
        center: [139.6225, 35.466111],//横浜駅
        zoom: 13,
    });

    map.on('load', () => {
        map.addSource('tile-grid', {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': []
            }
        });

        map.addLayer({
            'id': 'tile-line',
            'type': 'line',
            'source': 'tile-grid',
            'paint': {
                'line-color': '#888',
                'line-width': 1
            }
        });
        map.addLayer({
            'id': 'tile-pane',
            'type': 'fill',
            'source': 'tile-grid',
            'paint': {
                'fill-color': '#FFF',
                'fill-opacity': 0
            }
        });
        const loadedFeatures: any[] = [];
        const updateTileGrid = (map: maplibregl.Map) => {

            const bounds = map.getBounds();

            const zoom = Math.round(map.getZoom()) + 2;
            const minX = Math.floor(long2tile(bounds.getWest(), zoom));
            const maxX = Math.ceil(long2tile(bounds.getEast(), zoom));
            const minY = Math.floor(lat2tile(bounds.getNorth(), zoom));
            const maxY = Math.ceil(lat2tile(bounds.getSouth(), zoom));

            const newFeatures = [];

            for (let x = minX; x <= maxX; x++) {
                for (let y = minY; y <= maxY; y++) {
                    const quadkey = tileXYToQuadKey(x, y, zoom);
                    //すでに作成したfeatureのquadkeyがあるか検索
                    const existingFeature = loadedFeatures.find(feature => feature.properties.quadkey === quadkey);
                    if (existingFeature) {
                        newFeatures.push(existingFeature);
                    } else {
                        //新しくfeatureを作成
                        const tileBounds = tile2bounds(x, y, zoom);
                        const feature = {
                            'type': 'Feature',
                            'geometry': {
                                'type': 'Polygon',
                                'coordinates': [[
                                    [tileBounds[0], tileBounds[1]],
                                    [tileBounds[2], tileBounds[1]],
                                    [tileBounds[2], tileBounds[3]],
                                    [tileBounds[0], tileBounds[3]],
                                    [tileBounds[0], tileBounds[1]]
                                ]]
                            },
                            'properties': {
                                'x': x,
                                'y': y,
                                'z': zoom,
                                'quadkey': quadkey
                            }
                        };
                        newFeatures.push(feature);
                        loadedFeatures.push(feature);
                    }

                }
            }


            const data = {
                'type': 'FeatureCollection',
                'features': newFeatures
            };
            const tileGrid = map.getSource('tile-grid') as GeoJSONSource;
            //todo: 型定義する
            //@ts-ignore
            tileGrid.setData(data);

        };

        map.on('move', () => updateTileGrid(map));
        map.on('zoom', () => updateTileGrid(map));

        updateTileGrid(map);

        map.on('click', 'tile-pane', (e: any) => {
            console.log('click');
            const properties = e.features[0].properties;
            const message = `XYZ: (${properties.x}, ${properties.y}, ${properties.z})<br>QuadKey: ${properties.quadkey}`;
            new Popup()
                .setLngLat(e.lngLat)
                .setHTML(message)
                .addTo(map);
        });

        map.on('mouseenter', 'tile-grid', () => {
            map.getCanvas().style.cursor = 'pointer';
        });

        map.on('mouseleave', 'tile-grid', () => {
            map.getCanvas().style.cursor = '';
        });
    });
});


</script>
<template>
    <div id="map"></div>
</template>
<style scoped>
#map {
    height: 100vh;
}
</style>