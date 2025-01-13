window.addEventListener('DOMContentLoaded', event => {
    var hrRecords = reportRAW['report']['origin']['hr'];

    hrRecords = hrRecords.filter((e) => isBetweenGlobalDates(e.time));

    let recordsHTML=''
    hrRecords.forEach(function (item) {
        recordsHTML+=`
        <tr>
            <td>${timeConverter(item.time)}</td>
            <td>${item.value}</td>
            <td>${item.device}</td>
        </tr>`
    });

    document.getElementById("heart-rate-datatable-records").innerHTML = recordsHTML;

    const heartRateDatatable = document.getElementById('heart-rate-datatable');
    if (heartRateDatatable) {
        new simpleDatatables.DataTable(heartRateDatatable);
    }

Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var heartRateChart = document.getElementById("heart-rate-chart");
new Chart(heartRateChart, {
  type: 'line',
  data: {
    labels: hrRecords.map((e) => timeConverter(e.time)),
    datasets: [{
      label: "Hear Rate Value",
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: hrRecords.map((e) => e.value),
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
          min: Math.min.apply(Math, hrRecords.map((o) => o.value )) -10,
          max: Math.max.apply(Math, hrRecords.map((o) => o.value )) + 10,
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
