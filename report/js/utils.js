function timeConverter(UNIX_timestamp) {
    // var a = new Date(UNIX_timestamp * 1000);
    // var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    // var year = a.getFullYear();
    // var month = months[a.getMonth()];
    // var date = a.getDate();
    // var hour = a.getHours();
    // var min = a.getMinutes();
    // var sec = a.getSeconds();
    // var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec;

    var time = new Date(UNIX_timestamp * 1000).toLocaleString();
    return time;
}

function getDeviceInfoById(id) {
    return {
        "212": {
            "name": "Miband 6",
            "description": "Miband is a smart wearable produced by the Chinese brand Xiaomi.",
            "keyHighlights": ["24-hour smart heart rate monitoring","Spo2 monitoring", "Alarms", "Personal activity intelligence", "Stress monitoring", "Workout records with GPS artifacts"]
        }
    }[id]
}

function getEnabled(value) {
    return {
        "0": "Disabled",
        "1": "Enabled"
    }[value]
}
