function createChartObject(chartElementName, graphData){
    return new Chart(document.getElementById(chartElementName).getContext('2d'), graphData);
}

function updateChartData(updatedGraphData, graphData, djangoDataName){
    updatedGraphData.shift();
    updatedGraphData.push(djangoDataName);
    graphData.data.datasets[0].data = updatedGraphData;
}

function initializeGraphData(chartHeader, min_val=0, max_val=100, currentStatusName="Current usage"){
    return graphData = {
        type: 'line',
        data: {
            labels: ['22s', '20s', '18s', '14s', '12s','10s', '8s', '6s', '4s', '2s', currentStatusName],
            datasets: [{
                fill: true,
                label: chartHeader,
                data: [0, 0, 0, 0, 0, 0,0,0,0,0,0],
                backgroundColor: [
                    'rgba(0, 195, 0, 0.45)',

                ],
                borderWidth: 1
            }]
        },
        options: {
            interaction: {
          intersect: false,
        },scales: {
                y: {
                    type: 'linear',
                    min: min_val,
                    max: max_val
                }
            }}
    }
}

var cpuUsageGraphData = initializeGraphData("CPU usage (in %)");
var cpuUsageChartObject = createChartObject("cpuUsageChart", cpuUsageGraphData);
var updatedCpuData = cpuUsageGraphData.data.datasets[0].data;


var ramUsageGraphData = initializeGraphData("RAM usage (in %)");
var ramUsageChartObject = createChartObject("ramUsageChart", ramUsageGraphData);
var updatedRamData = ramUsageGraphData.data.datasets[0].data;


var networkUsageGraphData = initializeGraphData("Network usage (in MB)", min_val=0, max_val=24);
var networkUsageChartObject = createChartObject("networkUsageChart", networkUsageGraphData);
var updatedNetworkData = networkUsageGraphData.data.datasets[0].data;

var diskUsage = document.getElementById("diskUsage");
var uptime = document.getElementById("uptime");


var socket = new WebSocket("ws://" + location.host + "/ws/graph/");
socket.onmessage = function (e){
    var djangoData = JSON.parse(e.data);

    updateChartData(updatedCpuData, cpuUsageGraphData, djangoData.cpuPercentageUsage);
    cpuUsageChartObject.update();

    updateChartData(updatedRamData, ramUsageGraphData, djangoData.ramPercentageUsage);
    ramUsageChartObject.update();

    updateChartData(updatedNetworkData, networkUsageGraphData, djangoData.networkUsage);
    networkUsageChartObject.update();

    diskUsage.innerText = djangoData.diskUsage;

    uptime.innerText = djangoData.uptime;

}