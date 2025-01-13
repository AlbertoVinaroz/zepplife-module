window.addEventListener('DOMContentLoaded', event => {
    var deviceRecords = reportRAW['report']['origin']['devices'];


    let recordsHTML = ''
    deviceRecords.forEach((item, index) => {

        var deviceStaticInfo = getDeviceInfoById("212");
        item.type = "212"
        recordsHTML += `
            <div class="container-fluid px-4">
                <div class="card-body">
                    <h3 class="card-title">${item.id}</h3>
                    <h6 class="card-subtitle text-${item.bindStatus == 1 ? 'success' : 'danger'}">${getEnabled(item.bindStatus)}</h6>
                    <div class="row">
                        <div class="col-lg-5 col-md-5 col-sm-6">
                            <div class="text-center"><img src="./assets/img/device_${item.type}.png" class="img-device"></div>
                        </div>
                        <div class="col-lg-7 col-md-7 col-sm-6">
                            <h4 class="box-title mt-5">${deviceStaticInfo.name}</h4>
                            <p>${deviceStaticInfo.description}</p>
                            <h3 class="box-title mt-5">Key Highlights</h3>
                            <ul class="list-unstyled">`
        deviceStaticInfo.keyHighlights.forEach( function (kh){
        recordsHTML+= `<li><i class="fa fa-check text-success"></i> ${kh}</li>`
        })
                            
        recordsHTML+= `
                            </ul>
                        </div>
                        <div class="col-lg-12 col-md-12 col-sm-12">
                            <h3 class="box-title mt-5">General Info</h3>
                            <div class="table-responsive">
                                <table id="device-datatable">
                                    <tbody id="device-datatable-records"></tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
        var tableHTML =`
        <tr>
            <td class="col-4">ID</td>
            <td>${item.id}</td>
        </tr>
        <tr>
            <td>SERIAL NUMBER</td>
            <td>${item.sn}</td>
        </tr>
         <tr>
            <td>MAC ADDRESS</td>
            <td>${item.address}</td>
        </tr>

         <tr>
            <td>FIRMWARE VERSION</td>
            <td>${item.firmwareVersion}</td>
        </tr>

         <tr>
            <td>BIND STATUS</td>
            <td>${item.bindStatus}</td>
        </tr>
        
         <tr>
            <td>BIND TIME</td>
            <td>${timeConverter(item.bindTime)} (${item.bindTime})</td>
        </tr>

         <tr>
            <td>SYNC DATA TIME</td>
            <td>${timeConverter(item.syncDataTime)} (${item.syncDataTime})</td>
        </tr>
        
         <tr>
            <td>SYNC DATA TIME HR</td>
            <td>${timeConverter(item.syncDataTimeHR)} (${item.syncDataTimeHR})</td>
        </tr>
        
         <tr>
            <td>AUTHKEY</td>
            <td>${item.authkey}</td>
        </tr>

        <tr>
            <td>HARDWARE VERSION</td>
            <td>${item.hardwareVersion}</td>
        </tr>

        <tr>
            <td>PRODUCT VERSION</td>
            <td>${item.productVersion}</td>
        </tr>

        <tr>
            <td>USER ID</td>
            <td>
                <a href="index.html">
                ${item.userId}
                </a>
            </td>
        </tr>
        `
        document.getElementById("device-list").innerHTML = recordsHTML;
        document.getElementById("device-datatable-records").innerHTML = tableHTML;

        const deviceDatatable = document.getElementById('device-datatable');
        if (deviceDatatable) {
            new simpleDatatables.DataTable(deviceDatatable);
        }
    });









});
