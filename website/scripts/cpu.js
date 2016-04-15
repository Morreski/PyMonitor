
function cpu() {
    var cpuDiv = document.getElementById("cpu-div");
    var es = new EventSource("http://localhost:1337/api/cpu");
    var monitors = [];

    es.addEventListener("message", function(evt){
        data = JSON.parse(evt.data);
        if(data.length != monitors.length) {
            for(i in data) {
                var meter = document.createElement("meter");
                var value = document.createElement("p");
                meter.max = 100;
                cpuDiv.appendChild(meter);
                cpuDiv.appendChild(value);
                monitors.push([meter, value]);
            }
        }

        for (i in data) {
            monitors[i][0].value = data[i];
            monitors[i][1].innerText = data[i];
        }
    })
}

cpu();
