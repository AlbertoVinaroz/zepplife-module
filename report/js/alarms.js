window.addEventListener('DOMContentLoaded', event => {
    var alarms = reportRAW['report']['origin']['alarm'];

    let alarmsHTML='';
    alarms.forEach((item) => {
      alarmsHTML+=`        
        <tr>
            <td>${timeConverter(item.time/1000)}</td>
            <td>${item.enabled === "1" ? "Enabled" : "Disabled" }</td>
        </tr>
        `
    });
    document.getElementById("alarm-records").innerHTML = alarmsHTML;

    const alarmDatatable = document.getElementById('alarm-datatable');
    if (alarmDatatable) {
        new simpleDatatables.DataTable(alarmDatatable);
    }
});
