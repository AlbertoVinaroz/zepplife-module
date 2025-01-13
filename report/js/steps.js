window.addEventListener('DOMContentLoaded', event => {
    var stepsReport = reportRAW['report']['origin']['steps'];

    stepsReport = stepsReport.filter((e) => isBetweenGlobalDates(Date.parse(e.date + " " + e.from)/1000));

    let stepsHTML=''
    stepsReport.forEach(function (item) {
      if(isBetweenGlobalDates(Date.parse(item.date + " " + item.from)/1000)){
        stepsHTML+=`
        <tr>
            <td>${item.date}</td>
            <td>${item.from}</td>
            <td>${item.to}</td>
            <td>${item.mode}</td>
            <td>${item.distance}</td>
            <td>${item.steps}</td>
            <td>${item.calories}</td>
        </tr>`
      }
    });

    document.getElementById("steps-datatable-records").innerHTML = stepsHTML;

    const stepsDatatable = document.getElementById('steps-datatable');
    if (stepsDatatable) {
        new simpleDatatables.DataTable(stepsDatatable);
    }

Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var stepsChart = document.getElementById("steps-chart");
new Chart(stepsChart, {
  type: 'line',
  data: {
    labels: stepsReport.map((e) => e.date),
    datasets: [{
      label: "Steps Value",
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
      data: stepsReport.map((e) => e.steps),
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
          min: Math.min.apply(Math, stepsReport.map((o) => o.steps )) - 5,
          max: Math.max.apply(Math, stepsReport.map((o) => o.steps )) + 5,
          maxTicksLimit: 10
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: false
    },
    zoom: {
      enabled: true,
      drag: true,
      speed: 0.1,
      threshold: 2
  }
  }
});




});
