window.addEventListener('DOMContentLoaded', event => {
    var sleepRecords = reportRAW['report']['origin']['sleep'];

    sleepRecords = sleepRecords.filter((e) => isBetweenGlobalDates(Date.parse(e.date + " " + e.from)/1000));
    let recordsHTML=''
    sleepRecords.forEach(function (item) {

      if(isBetweenGlobalDates(Date.parse(item.date + " " + item.from)/1000)){
        recordsHTML+=`
        <tr>
            <td>${item.date}</td>
            <td>${item.from}</td>
            <td>${item.to}</td>
            <td>${item.mode}</td>
        </tr>`
      }
    });

    document.getElementById("sleep-datatable-records").innerHTML = recordsHTML;

    const sleepDatatable = document.getElementById('sleep-datatable');
    if (sleepDatatable) {
        new simpleDatatables.DataTable(sleepDatatable);
    }
});
