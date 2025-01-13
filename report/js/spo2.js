window.addEventListener('DOMContentLoaded', event => {
    var spoRecords = reportRAW['report']['spo']['spo'];

    spoRecords = spoRecords.filter((e) => isBetweenGlobalDates(e.time));

    let recordsHTML=''
    spoRecords.forEach(function (item) {
        recordsHTML+=`
        <tr>
            <td>${timeConverter(item.time)}</td>
            <td>${item.value}</td>
            <td>${item.device}</td>
        </tr>`
    });

    document.getElementById("spo-datatable-records").innerHTML = recordsHTML;

    const spoDatatable = document.getElementById('spo-datatable');
    if (spoDatatable) {
        new simpleDatatables.DataTable(spoDatatable);
    }

Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var spoChart = document.getElementById("spo-chart");
new Chart(spoChart, {
  type: 'line',
  data: {
    labels: spoRecords.map((e) => timeConverter(e.time)),
    datasets: [{
      label: "Spo2 Value",
      lineTension: 0.3,
      backgroundColor: "rgba(240,1,10,0.2)",
      borderColor: "rgba(240,1,10,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(240,1,10,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(240,1,10,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: spoRecords.map((e) => e.value),
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          min: Math.min.apply(Math, spoRecords.map((o) => o.value )) -10,
          max: Math.max.apply(Math, spoRecords.map((o) => o.value )) + 10,
          maxTicksLimit: 10
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: false
    }
  }
});




});
