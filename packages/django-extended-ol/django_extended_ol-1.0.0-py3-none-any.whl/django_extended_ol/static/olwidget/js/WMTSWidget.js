/* global ol */
'use strict';

class WMTSWidget extends MapWidget {
    createMap() {
        this.map_extent = this.options.extent;
        this.projection = new ol.proj.Projection({
            code: `EPSG:${this.options.map_srid}`,
            extent: this.map_extent,
        });
        return new ol.Map({
            target: this.options.map_id,
            layers: [this.options.base_layer],
            view: new ol.View({
                center: this.options.default_center,
                resolution: this.options.default_resolution,
                projection: this.projection,
                resolutions: this.options.resolutions,
                constrainResolution: true
            })
        });
    }

    defaultCenter() {
        return this.options.default_center;
    }
}
