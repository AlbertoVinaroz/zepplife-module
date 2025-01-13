function saveOnLocalStorage(key, value){
    localStorage.setItem(key, Date.parse(value)/1000)
    document.getElementById(key).value = new Date(localStorage.getItem(key) * 1000).toISOString().slice(0,16);
    location.reload();
}

function clearLocalStorageDates(){
    localStorage.removeItem("global-to");
    localStorage.removeItem("global-from");
    saveOnLocalStorage("global-to", new Date());
    saveOnLocalStorage("global-from", new Date(1388534400000));
}

function globalFrom(){
    let value = localStorage.getItem('global-from');
    return value ? value :  document.getElementById("global-from").value = new Date(1388534400000).toISOString().slice(0,16);
}

function globalTo(){
    let value = localStorage.getItem('global-to');
    return value ? value :  document.getElementById("global-to").value = new Date().toISOString().slice(0,16);
}

function isBetweenGlobalDates(date){
    return (date > globalFrom() && date < globalTo())
}

function populateCaseDetails(caseDetails){
    document.getElementById('caseDate').innerHTML = timeConverter(caseDetails?.caseDate);
    document.getElementById('caseNumber').value =  caseDetails?.number;
    document.getElementById('caseName').value =  caseDetails?.examinerName;
    document.getElementById('casePhone').value =  caseDetails?.examinerPhone;
    document.getElementById('caseEmail').value =  caseDetails?.examinerEmail;
    document.getElementById('caseNotes').value =  caseDetails?.examinerNotes;
    
}

window.addEventListener('DOMContentLoaded', event => {

    var caseDetails = reportRAW['case'];

    document.getElementById("mf-navbar").innerHTML = 
    `
    <nav class="sb-topnav navbar navbar-expand navbar-dark bg-dark">
    <!-- Navbar Brand-->
    <a class="navbar-brand ps-3" href="index.html">MiFit/Zepp Life Analysis</a>
    <!-- Sidebar Toggle-->
    <button class="btn btn-link btn-sm order-1 order-lg-0 me-4 me-lg-0" id="sidebarToggle" href="#!"><i class="fas fa-bars"></i></button>
    
    <div class="container">
        <div class="row">
        <div class="col col-1">
            <label class="text-white mt-1">From:</label>
        </div>
            <div class="col col-4">
                <input onblur="saveOnLocalStorage('global-from', this.value);" id="global-from" type="datetime-local" class="form-control" name="from">
            </div>
        <div class="col col-1">
            <label class="text-white mt-1">To:</label>
        </div>
        <div class="col-4">
            <input onblur="saveOnLocalStorage('global-to', this.value);" id="global-to" type="datetime-local" class="form-control" name="to">
        </div>
        <div class="col-2 p-0">
            <button type="button" onclick="clearLocalStorageDates()" class="btn btn-primary">Clear Dates</button>
        </div>
      </div>
    </div>
    
    </nav>
    <div id="layoutSidenav_nav">
        <nav class="sb-sidenav accordion sb-sidenav-dark" id="sidenavAccordion">
            <div class="sb-sidenav-menu">
                <div class="nav">
                    <div class="sb-sidenav-menu-heading">Core</div>
                    <a class="nav-link" href="index.html">
                        <div class="sb-nav-link-icon"><i class="fas fa-users"></i></div>
                        Profiles
                    </a>
                    <a class="nav-link" href="device.html">
                        <div class="sb-nav-link-icon"><i class="fas fa-mobile"></i></div>
                        Devices
                    </a>
                    <div class="sb-sidenav-menu-heading">Artifacts</div>
                    <div>
                        <nav class="sb-sidenav-menu-nested nav">
                        <a class="nav-link" href="heart-rate.html">
                        <div class="sb-nav-link-icon"><i class="fas fa-heartbeat"></i></div>
                        Heart Rate
                        </a>
                        <a class="nav-link" href="sleep.html">
                        <div class="sb-nav-link-icon"><i class="fas fa-bed"></i></div>
                        Sleep
                        </a>
                        <a class="nav-link" href="alarms.html">
                        <div class="sb-nav-link-icon"><i class="fas fa-clock"></i></div>
                        Alarms
                        </a>
                        <a class="nav-link" href="workouts.html">
                        <div class="sb-nav-link-icon"><i class="fas fa-dumbbell"></i></div>
                        Workouts
                        </a>
                        <a class="nav-link" href="steps.html">
                        <div class="sb-nav-link-icon"><i class="fas fa-shoe-prints"></i></div>
                        Steps
                        </a>
                        <a class="nav-link" href="stress.html">
                        <div class="sb-nav-link-icon"><i class="fas fa-frown-open"></i></div>
                        Stress
                        </a>
                        <a class="nav-link" href="spo2.html">
                        <div class="sb-nav-link-icon"><i class="fas fa-heartbeat"></i></div>
                        Spo2
                        </a>
                        </a>
                        <a class="nav-link" href="female.html">
                        <div class="sb-nav-link-icon"><i class="fas fa-female"></i></div>
                        Female Health
                        </a>
                        </nav>
                    </div>
                </div>
            </div>
            <div class="sb-sidenav-footer">
                <div class="small">Report created at: <span id="caseDate"> </span> </div>
                    <a class="btn btn-link" type="button" data-bs-toggle="collapse" data-bs-target="#collapseCase" aria-expanded="false" aria-controls="collapseCase">
                        See case details
                    </a>
                    <div class="collapse" id="collapseCase">
                    <div class="input-group mb-3">
                        <div class="input-group input-group-sm mb-3">
                            <span class="input-group-text" id="inputGroup-sizing-sm">Case</span>
                            <input id="caseNumber" type="text" class="form-control" disabled>
                        </div>
                        <div class="input-group input-group-sm mb-3">
                            <span class="input-group-text" id="inputGroup-sizing-sm">Name</span>
                            <input id="caseName" type="text" class="form-control" disabled>
                        </div>
                        <div class="input-group input-group-sm mb-3">
                            <span class="input-group-text" id="inputGroup-sizing-sm">Phone</span>
                            <input id="casePhone" type="text" class="form-control" disabled>
                        </div>
                        <div class="input-group input-group-sm mb-3">
                            <span class="input-group-text" id="inputGroup-sizing-sm">Email</span>
                            <input id="caseEmail" type="text" class="form-control" disabled>
                        </div>
                        <div class="input-group input-group-sm mb-3">
                            <span class="input-group-text" id="inputGroup-sizing-sm">Notes</span>
                            <textarea id="caseNotes" type="text" class="form-control" disabled></textarea>
                        </div>
                    </div>
            </div>
        </nav>
    </div>
    `;

    const sidebarToggle = document.body.querySelector('#sidebarToggle');  
    
    document.getElementById('global-from').value = new Date(localStorage.getItem('global-from') * 1000).toISOString().slice(0,16);
    document.getElementById('global-to').value = new Date(localStorage.getItem('global-to') * 1000).toISOString().slice(0,16);
    
    populateCaseDetails(caseDetails);
   
    if (sidebarToggle) {
        if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
            document.body.classList.toggle('sb-sidenav-toggled');
        }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});