import { getCoordinatesFromImgUrl } from './exifUtils';
import { longLatToQuadKey } from './tileUtils'
export async function setImgData() {
    const imgData = [];
    const imageRecord = await import.meta.glob('/src/assets/resized_image/*.jpg');
    const imageList = Object.keys(imageRecord);


    for (const [index, image] of imageList.entries()) {
        const coordinates = await getCoordinatesFromImgUrl(image);
        if (coordinates) {
            const quadKey = longLatToQuadKey(coordinates[0], coordinates[1]);

            imgData.push({
                url: image,
                quadKey: quadKey,
            });
        }
    }
    return imgData;
};