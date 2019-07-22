function add_percent(value, perc) {
    value += value * perc / 100;
    return value;
}

document.
    addEventListener("DOMContentLoaded",
		     function (event) {

			 var output = document.querySelector("#output");
			 output.style.display = "none";

			 function Data() {
			     this.years = 4;
			     this.init_summ = 15000000;
			     this.capital_increase = 10;
			     this.init_salary = 2500000;
			     this.salary_increase = 7;
			 }			 

			 function setNumberById(id, number) {
			     document.querySelector(id).value = number;
			 }

			 function fillDefaults(defaults) {
			     setNumberById("#years", defaults.years);
			     setNumberById("#init_summ", defaults.init_summ);
			     setNumberById("#capital_increase", defaults.capital_increase);
			     setNumberById("#init_salary", defaults.init_salary);
			     setNumberById("#salary_increase", defaults.salary_increase);
			 }

			 var init_by_ajax = false;
			 var data = new Data();

			 if (init_by_ajax) {
			     ajaxUtils
				 .sendGetRequest("data/defaults.json", fillDefaults);
			 }
			 else {
			     fillDefaults(data);
			 }			     

			 function parseNumberById(id) {
			     return Number(document.querySelector(id).value);
			 }

			 function parseData() {
			     data.years = parseNumberById("#years");
     		     	     data.init_summ = parseNumberById("#init_summ");
                             data.capital_increase = parseNumberById("#capital_increase");
			     data.init_salary = parseNumberById("#init_salary");
			     data.salary_increase = parseNumberById("#salary_increase");
			 }

 		     	 function calculate() {
			     parseData();
			     
			     var summ = data.init_summ;
			     var salary = data.init_salary;

			     yearly_results = [];

			     for (var i = 0; i < data.years; i++) {				 
				 summ = add_percent(summ, data.capital_increase);
				 summ += salary;
				 salary = add_percent(salary, data.salary_increase);
				 yearly_results[i] = summ;
			     }

			     return yearly_results;
		     	 }

			 function outputResults(yearly) {
			     var out_region = document.querySelector("#output");
			     out_region.innerHTML = "<p>Результат:</p>";

			     for (var i = 0; i < yearly.length; i++) {
				 var line = "Год " + (i + 1) + ": " + yearly[i];
				 out_region.innerHTML += "<p>" + line + "</p>";
			     }
			 }
			 
			 function doWork(event) {
			     results = calculate();
			     outputResults(results);
			     output.style.display = "block";
			 }

			 document.querySelector("button").addEventListener("click", doWork);
		     }

		    )
