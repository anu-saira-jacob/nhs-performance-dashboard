window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
                const q = feature.properties.imd_quintile;
                const colors = {
                    1: '#7f0000',
                    2: '#b30000',
                    3: '#e34a33',
                    4: '#fc8d59',
                    5: '#fdcc8a'
                };
                return {
                    color: '#666',
                    weight: 0.5,
                    fillOpacity: 0.75,
                    fillColor: colors[q] || '#cccccc'
                };
            }

            ,
        function1: function(feature, context) {
                return {
                    color: '#3f3d3d',
                    weight: 1.5,
                    opacity: 0.95,
                    fill: true, // <— enable fill to capture mouse events over the area
                    fillOpacity: 0.0, // <— fully transparent; still hit-testable
                };
            }

            ,
        function2: function(feature, layer, context) {
                const label = feature.properties.icb_label || feature.properties.icb_name || '';
                layer.bindTooltip(label, {
                    sticky: true,
                    direction: 'top'
                });
            }

            ,
        function3: function(feature, context) {
                return {
                    color: '#1f2937', // darker charcoal
                    weight: 2.5
                };
            }

            ,
        function4: function(feature, context) {
            return {
                color: '#193758', // darker charcoal
                weight: 3,
                opacity: 1,
                fill: true,
                fillOpacity: 0.0
            };
        }

    }
});