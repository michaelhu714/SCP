// clientside.js
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_satellites: function(sat_data, fig) {
            if (!fig || !sat_data) {
                return fig;
            }

            for (var i = 0; i < sat_data.length; i++) {
                var sat = sat_data[i];
                var trace_index = i + 2;  // earth=0, stars=1

                if (fig.data[trace_index]) {
                    fig.data[trace_index].x = [sat.x];
                    fig.data[trace_index].y = [sat.y];
                    fig.data[trace_index].z = [sat.z];
                }
            }

            return fig;
        }
    }
});
