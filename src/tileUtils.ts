export function long2tile(lon: number, zoom: number): number {
    return Math.floor((lon + 180) / 360 * Math.pow(2, zoom));
}

export function lat2tile(lat: number, zoom: number): number {
    return Math.floor((1 - Math.log(Math.tan(lat * Math.PI / 180) + 1 / Math.cos(lat * Math.PI / 180)) / Math.PI) / 2 * Math.pow(2, zoom));
}

export function tile2bounds(x: number, y: number, z: number): [number, number, number, number] {
    const n = Math.pow(2, z);
    const lon1 = x / n * 360 - 180;
    const lat1 = Math.atan(Math.sinh(Math.PI * (1 - 2 * y / n))) * 180 / Math.PI;
    const lon2 = (x + 1) / n * 360 - 180;
    const lat2 = Math.atan(Math.sinh(Math.PI * (1 - 2 * (y + 1) / n))) * 180 / Math.PI;
    return [lon1, lat1, lon2, lat2];
}

export function tileXYToQuadKey(x: number, y: number, z: number): string {
    let quadKey = '';
    for (let i = z; i > 0; i--) {
        let digit = 0;
        const mask = 1 << (i - 1);
        if ((x & mask) !== 0) {
            digit++;
        }
        if ((y & mask) !== 0) {
            digit += 2;
        }
        quadKey += digit;
    }
    return quadKey;
}

export function longLatToQuadKey(lon: number, lat: number): string {
    const zoom = 24; // Adjust zoom level as needed (higher zoom for more detailed tiles)
    const tileX = long2tile(lon, zoom);
    const tileY = lat2tile(lat, zoom);
    return tileXYToQuadKey(tileX, tileY, zoom);
}