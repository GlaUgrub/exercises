function add_percent(value, perc) {
    value += value * perc / 100;
    return value;
}

document.
    addEventListener("DOMContentLoaded",
		     function (event) {

			 function setNumberById(id, number) {
			     document.querySelector(id).value = number;
			 }

			 function applyDefaults(defaults) {
			     setNumberById("#years", defaults.years);
			     setNumberById("#init_summ", defaults.init_summ);
			     setNumberById("#capital_increase", defaults.capital_increase);
			     setNumberById("#init_salary", defaults.init_salary);
			     setNumberById("#salary_increase", defaults.salary_increase);
			 }

			 ajaxUtils
			     .sendGetRequest("data/defaults.json", applyDefaults);

			 function parseNumberById(id) {
			     return Number(document.querySelector(id).value);
			 }


 		     	 function calculate(event) {
			     var years = parseNumberById("#years");

			     var given = {};
		     	     given.init_summ = parseNumberById("#init_summ");
                             given.capital_increase = parseNumberById("#capital_increase");
			     given.init_salary = parseNumberById("#init_salary");
			     given.salary_increase = parseNumberById("#salary_increase");

			     var summ = given.init_summ;
			     var salary = given.init_salary;

			     yearly_results = [];

			     for (var i = 0; i < years; i++) {				 
				 summ = add_percent(summ, given.capital_increase);
				 summ += salary;
				 salary = add_percent(salary, given.salary_increase);
				 yearly_results[i] = summ;
			     }

			     return yearly_results;
		     	 }

			 function outputResults(event, yearly) {
			     var out_region = document.querySelector("#output");
			     out_region.innerHTML = "<p>Результат:</p>";

			     for (var i = 0; i < yearly.length; i++) {
				 var line = "Год " + (i + 1) + ": " + yearly[i];
				 out_region.innerHTML += "<p>" + line + "</p>";
			     }
			 }
			 
			 function doWork(event) {
			     results = calculate(event);
			     outputResults(event, results);
			 }

			 document.querySelector("button").addEventListener("click", doWork);
		     }

		    )
