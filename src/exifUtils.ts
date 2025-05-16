import exifr from 'exifr';
export async function getCoordinatesFromImgUrl(url: string) {

    const exifData = await exifr.parse(url);

    if (exifData && exifData.latitude && exifData.longitude) {
        const lat = exifData.latitude;
        const lon = exifData.longitude;
        return [lon, lat];
    } else {
        return null;
    }

};