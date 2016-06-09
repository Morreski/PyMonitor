var monitors = [];
var disks = [];

function cpu() {
  var cpuDiv = document.getElementById("cpu-div");
  var es = new EventSource("http://localhost:1337/api/cpu");

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

function ram() {
    var diskDiv = document.getElementById("disks-div");
    var es = new EventSource("http://localhost:1337/api/disks");
    es.onmessage = function(evt) {
        data = JSON.parse(evt.data);
        if(Object.keys(data).length != disks.length) {
          for(_ in data) {
            var meter = document.createElement("meter");
            var value = document.createElement("p");
            meter.max = 100;
            diskDiv.appendChild(meter);
            diskDiv.appendChild(value);
            disks.push([meter, value]);
          }
        }

        var i = 0;
        for(diskName in data) {
          disks[i][0].value = data[diskName];
          disks[i][1].innerText = diskName;
          i++;
        }
    }
}

cpu();
ram();
