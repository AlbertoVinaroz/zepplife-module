window.addEventListener('DOMContentLoaded', event => {
    var profiles = reportRAW['report']['users']['userInfo'];
    var user_details = reportRAW['report']['origin']['userDetails'];

    let profilesHTML=`<h1 class="mt-4">${profiles.length} user profile(s) found:</h1>`;
    profiles.forEach((item) => {
      
      profilesHTML+=`       
        <div class="row">
            <div class="col-3 border-right">
                <div class="d-flex flex-column align-items-center text-center p-3 py-5"><img class="rounded-circle mt-5" width="150px" src="${user_details.avatar}"><h5 class="mt-2 font-weight-bold">${user_details.name}</h5><span class="text-black-50">${item.email}</span>
                    <div class="mt-3">
                        <span class="text-black-50">Height: ${user_details.height}cm</span>
                        <span class="text-black-50">Weight: ${user_details.weight}Kg</span>
                    </div>
                </div>
            </div>
            <div class="col-5 border-right">
                <div class="p-3 py-5">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="text-right">Profile Settings</h4>
                    </div>
                    <div class="row mt-2">
                        <div class="mt-2 col-8"><label class="labels">Nickname</label><span class="form-control">${user_details.name}</span></div>
                        <div class="mt-2 col-4"><label class="labels">Country</label><span class="form-control">${item.countryCode}</span></div>
                        <div class="mt-2 col-12"><label class="labels">Email</label><span class="form-control">${item.email}</span></div>
                        <div class="mt-2 col-6"><label class="labels">Provider</label><span class="form-control">${item.provider}</span></div>
                        <div class="mt-2 col-6"><label class="labels">Provider ID</label><span class="form-control">${item.thirdId}</span></div>
                        <div class="mt-2 col-12"><label class="labels">Regist Date</label><span class="form-control">${timeConverter(item.registDate / 1000)} (${item.registDate})</span></div>
                        <div class="mt-2 col-12"><label class="labels">App Token</label><textarea class="form-control">${item.appToken}</textarea></div>
                        <div class="mt-2 col-12"><label class="labels">Login Token</label><textarea class="form-control">${item.loginToken}</textarea></div>
                        <div class="mt-2 col-12"><label class="labels">Id Token</label><span class="form-control">${item.idToken}</span></div>
                    </div>
                </div>
            </div>
        </div>
        `


    });
    document.getElementById("profiles").innerHTML = profilesHTML;
});
