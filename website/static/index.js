// this javascript is already linked in base.html
// when needed use this file for your js codes

// ROCKETS //
function delete_rocket(rocket_id) {
    document.location = '/delete_rocket?rocket_id=' + rocket_id
}
function delete_rocket_d1(rocket_id) {
    document.location = '/delete_rocket_detail_1?rocket_id=' + rocket_id
}
function delete_rocket_d2(rocket_id) {
    document.location = '/delete_rocket_detail_2?rocket_id=' + rocket_id
}
function delete_rocket_image(rocket_id) {
    document.location = '/delete_rocket_image?rocket_id=' + rocket_id
}
//CORES//
function delete_core(core_id) {
    document.location = '/delete_core?core_id=' + core_id
}

// PAYLOADS //
function delete_payload(payload_id) {
    document.location = '/delete_payload?payload_id=' + payload_id
}

//LAUNCHES//
function delete_launch(launch_id) {
    document.location = '/delete_launch?launch_id=' + launch_id
}

function delete_launch_detail(launch_id) {
    document.location = '/delete_launch_detail?launch_id=' + launch_id
}
//SHIPS//
function delete_ship(ship_id) {
    document.location = '/delete_ship?ship_id=' + ship_id
}
function delete_ship_d1(ship_id) {
    document.location = '/delete_ship_detail_1?ship_id=' + ship_id
}
function delete_ship_d2(ship_id) {
    document.location = '/delete_ship_detail_2?ship_id=' + ship_id}