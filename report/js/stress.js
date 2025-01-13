window.addEventListener('DOMContentLoaded', event => {
    var stressReport = reportRAW['report']['stress']['allDayStress'];

    stressReport = stressReport.filter((e) => isBetweenGlobalDates(e.time/1000));

    let stressHTML=''
    stressReport.forEach(function (item) {
        stressHTML+=`
        <tr>
            <td>${timeConverter(item.time)}</td>
            <td>${item.value}</td>
        </tr>`
    });

    document.getElementById("stress-datatable-records").innerHTML = stressHTML;

    const stressDatatable = document.getElementById('stress-datatable');
    if (stressDatatable) {
        new simpleDatatables.DataTable(stressDatatable);
    }

Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var stressChart = document.getElementById("stress-chart");
new Chart(stressChart, {
  type: 'line',
  data: {
    labels: stressReport.map((e) => timeConverter(e.time)),
    datasets: [{
      label: "Stress Value",
      lineTension: 0.3,
      backgroundColor: "rgba(1,200,10,0.2)",
      borderColor: "rgba(1,200,10,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(1,200,10,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: stressReport.map((e) => e.value),
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
          min: Math.min.apply(Math, stressReport.map((o) => o.value )) - 5,
          max: Math.max.apply(Math, stressReport.map((o) => o.value )) + 5,
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
