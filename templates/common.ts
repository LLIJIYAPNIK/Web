import type {YMapLocationRequest, LngLat} from '@yandex/ymaps3-types';

export const LOCATION: YMapLocationRequest = {
  center: [37.623082, 55.75254], // starting position [lng, lat]
  zoom: 9 // starting zoom
};

// Array containing data for markers
export const markerProps = [
  {
    coordinates: [37.623, 55.752] as LngLat,
    iconSrc:
      'https://yastatic.net/s3/front-maps-static/maps-front-jsapi-3/examples/images/marker-custom-icon/yellow-capybara.png',
    message: "I'm yellow capybara!"
  },
  {
    coordinates: [38.125, 55.622] as LngLat,
    iconSrc:
      'https://yastatic.net/s3/front-maps-static/maps-front-jsapi-3/examples/images/marker-custom-icon/purple-capybara.png',
    message: "I'm purple capybara!"
  },
  {
    coordinates: [37.295, 55.415] as LngLat,
    iconSrc:
      'https://yastatic.net/s3/front-maps-static/maps-front-jsapi-3/examples/images/marker-custom-icon/green-capybara.png',
    message: "I'm green capybara!"
  }
];
