/*global $*/
// initialize variables for interval of refreshing
var minutes = 60;
var milliseconds = min_to_ms(minutes);

// function that converts minutes to milliseconds for use in update_interval function
function min_to_ms(min) {
    return min*60*1000;
}

// update open data block
function update_open_data() {
    $.getJSON("https://www.chapelhillopendata.org/api/datasets/1.0/search?rows=1&apikey=" + ODS_api + "&callback=?", function(datasets){
        // set number of datasets
        $('#numD').text(datasets.nhits);
    });
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/analyze/?dataset=ods-datasets-monitoring&source=monitoring&y.total_records.expr=records_count&y.total_records.func=SUM&apikey=" + ODS_api + "&callback=?", function(records){
        // set number of records total
        $('#numR').text(records[0].total_records);
    });
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/analyze/?dataset=ods-api-monitoring&source=monitoring&x=user_ip_addr&x=user_id&y.serie1.func=COUNT&apikey=" + ODS_api + "&callback=?", function(users){
        // set number of users total
        $('#numU').text(users.length);
    });
    
}

// update permit data
function update_permits() {
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/download/?dataset=permits&format=json&apikey=" + ODS_api + "&callback=?", function(today){
        // save counters and current date in variables
        var m_count = 0;
        var d_count = 0;
        var d = new Date();
        var current_month = d.getMonth() + 1;
        var current_year = d.getFullYear();
        var current_day = d.getDate();
        
        // loop through data and increment counter accordingly
        for(var i = 0; i < today.length; i++) {
            var date = today[i].fields.issue_date.split('/');
            if(date[0] == current_month && date[2] == current_year) {
                m_count+=1;
            }
            if(date[0] == current_month && date[1] == current_day && date[2] == current_year) {
                d_count+=1;
            }
        
        }
        $('#issuedMonth').text(m_count);
        $('#issuedToday').text(d_count);
    });    
}

// update number of datasets
function update_catalog_data() {
    var temp;
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=daily-catalog-searches&sort=column_2&apikey=" + ODS_api + "&callback=?", function(dailyCat){
        // save top searches today in variable
        temp = dailyCat.records[0].fields.column_1;
        $('#topCatToday').text(temp);
    });      
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=monthly-library-catalog-searches&sort=column_2&apikey=" + ODS_api + "&callback=?", function(monthlyCat){
        // save top searches this month in variable
        temp = monthlyCat.records[0].fields.column_1;
        $('#topCatMonth').text(temp);
    });   
}

// update website data info
function update_site_data() {
    var variable;
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=daily-sessions-chpl-website&apikey=" + ODS_api + "&callback=?", function(daily_sessions){
        // save amount of sessions today in variable
        variable = daily_sessions.records[0].fields.column_2;
        $('#sToday').text(variable);
    });
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=monthly-sessions-chpl-website&apikey=" + ODS_api + "&callback=?", function(monthly_sessions){
        // save amount of sessions this month in variable
        variable = monthly_sessions.records[0].fields.column_2;
        $('#sMonth').text(variable);
    });
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=dailysearch&sort=column_2&apikey=" + ODS_api + "&callback=?", function(daily_search){
        // save top searches today in variable
        variable = daily_search.records[0].fields.column_1;
        $('#topToday').text(variable);
    });
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=monthlysearch&sort=column_2&apikey=" + ODS_api + "&callback=?", function(monthly_search){
        // save top searches this month in variable
        variable = monthly_search.records[0].fields.column_1;
        $('#topMonth').text(variable);
    });
}

// update patron info
function update_patrons() {
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=patron-data&apikey=" + ODS_api + "&callback=?", function(patron_data){
        // save average age of unexpired patrons in variable
        var age = patron_data.records[0].fields.average_age;
        var blocked = patron_data.records[0].fields.blocked_patrons;
        $('#avg-age').text(Math.round(age));
        $('#blocked').text(blocked);
    });
}

// update items info
function update_items() {
    var total_checked_out = 0;
    $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=overdue-items&rows=1&apikey=" + ODS_api + "&callback=?", function(od_items) {
        // add amount of overdue items to checked out items
        $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=checked-out-items&rows=1&apikey=" + ODS_api + "&callback=?", function(co_items) {
            total_checked_out = co_items.nhits+od_items.nhits;
            $('#checked').text(total_checked_out);
            $.getJSON("https://www.chapelhillopendata.org/api/records/1.0/search/?dataset=library-items&rows=1&facet=status&refine.status=AVAILABLE&apikey=" + ODS_api + "&callback=?", function(total_a) {
                $('#totalAvailable').text(total_a.nhits - total_checked_out);
                $('#items-percent-out').text((total_checked_out/total_a.nhits*100).toFixed(2));
            });
        });
        
        $('#overdue').text(od_items.nhits);
    });
}

// function that gets a json and updates the page 
function update_page() {
    // gets local json file
    /*global $*/
    /*global ODS_api*/
    /*global circulator_location*/
    
    // update Open Data info
    update_open_data();
    
    // update Permit info
    update_permits();
    
    // update catalog info
    update_catalog_data();
    
    // update website info
    update_site_data();
 
    // update patron info
    update_patrons();
    
    // update items info
    update_items();
    
    // display updated date
    var d = new Date();
    var offset = -300;
    var estDate = new Date(d.getTime() + offset*60*1000);
    var uDate = estDate.toUTCString().replace('GMT', '');
    $('#stamp').text('Updated: ' + uDate);
}

// function that calls update_page every specified minutes
function update_interval(interval) {
    var update = setInterval(update_page, interval);
}

// call update_page to get the initial values
update_page();

// call update_interval to display the data and start timer
update_interval(milliseconds);