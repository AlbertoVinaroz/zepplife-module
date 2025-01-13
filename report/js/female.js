window.addEventListener('DOMContentLoaded', event => {
    var historyRecords = reportRAW['report']['female']['history'];

    let historyRecordsHTML='';
    historyRecords.forEach((item) => {
        historyRecordsHTML+=`        
        <tr>
            <td>${timeConverter(item.start/1000)}</td>
            <td>${timeConverter(item.end/1000)}</td>
        </tr>
        `
    });
    document.getElementById("fh-history-menstruation-records").innerHTML = historyRecordsHTML;

    const historyRecordsDatatable = document.getElementById('fh-history-menstruation-datatable');
    if (historyRecordsDatatable) {
        new simpleDatatables.DataTable(historyRecordsDatatable);
    }

    // ---

    var femaleRecords = reportRAW['report']['female']['records'];

    let femaleRecordsHTML='';
    femaleRecords.forEach((item) => {
        femaleRecordsHTML+=`        
        <tr>
            <td>${timeConverter(item.updateTime/1000)}</td>
            <td>${timeConverter(item.date/1000)}</td>
        </tr>
        `
    });
    document.getElementById("fh-menstruation-records").innerHTML = femaleRecordsHTML;

    const femaleRecordsDatatable = document.getElementById('fh-menstruation-datatable');
    if (femaleRecordsDatatable) {
        new simpleDatatables.DataTable(femaleRecordsDatatable);
    }

    // ---

    var symptomsRecords = reportRAW['report']['female']['symptoms'];

    let symptomsRecordsHTML='';
    symptomsRecords.forEach((item) => {
        symptomsRecordsHTML+=`        
        <tr>
            <td>${timeConverter(item.date/1000)}</td>
            <td>${item.type}</td>
        </tr>
        `
    });
    document.getElementById("fh-symptoms-records").innerHTML = symptomsRecordsHTML;

    const symptomsRecordsDatatable = document.getElementById('fh-symptoms-datatable');
    if (symptomsRecordsDatatable) {
        new simpleDatatables.DataTable(symptomsRecordsDatatable);
    }


});
