/** This is the automated test script used within Postman 
 * Every time a user tries out our API using Postman's 
 * interface, these tests run in the 'Tests' tab to ensure
 * that tests are still passing.
 * 
 * These scripts pass for every response code type (shown in 
 * Testing Documentation)
 * */ 

// Check that only error codes that we want to let through are passing
tests["Status code is 200, 400 or 404"] = responseCode.code === 200 || responseCode.code === 400 || responseCode.code === 404;

// Checks appropriate format for 200 responses.
if (responseCode.code === 200) {
    pm.test("200 Response is an array of articles",() => {
    let jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array');
    pm.expect(jsonData.length > 0);
    });

    pm.test("200 Response has appropriate keys",() => {
        pm.expect(pm.response.text()).to.include("url");
        pm.expect(pm.response.text()).to.include("date_of_publication");
        pm.expect(pm.response.text()).to.include("headline");
        pm.expect(pm.response.text()).to.include("datetime_accessed");
        pm.expect(pm.response.text()).to.include("main_text");
        pm.expect(pm.response.text()).to.include("reports");
    });
// Checks appropriate format for 400 responses.
} else if (responseCode.code === 400) {
    pm.test("400 Response has appropriate keys",() => {
        pm.expect(pm.response.text()).to.include("reason");
    });
// Checks appropriate format for 404 responses.
} else if (responseCode.code === 404) {
    pm.test("404 Response has appropriate reason",() => {
        pm.expect(pm.response.text()).to.include("Filtered data for location/disease returned no matching articles.");
    });
}