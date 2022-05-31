function request(path,
    worker=(response, details, code) => {
        console.log(code);
        console.log(response)
    },
    worker_details={})
{
    var xmlhttp = new XMLHttpRequest();
    
    xmlhttp.onreadystatechange = function() 
    {
        if (this.readyState == 4) {
            if (this.status == 200)
            {
                var myArr = JSON.parse(this.responseText);
                worker(myArr, worker_details, this.status);
            }
            else { worker(null, worker_details, this.status); }
        }
    };
    xmlhttp.open("GET", path, false);
    xmlhttp.send();
}

var states = {};
var current_job = null;
var refresh_timer = null;


function get_state(id, details={})
{
    worker = (response, details, code) => {
        if (code == 200)
        {
            states[id] = response;
            if (details.callback)
                details.callback(response);
        }
        if (code == 404)
            alert("No job found with requested ID")
    };
    request(`/get-state/${id}`, worker, details);
}


function submit_job(target, max_ttl, timeout, details={})
{
    worker = (response, details, code) => {
        if (code == 200)
        {
            var id = 1 * response;
            current_job = id

            if (details.callback)
                details.callback(id);
        }
        if (code == 400)
        {
            alert("Bad target specified!")
        }
    }
    request(`/trace?target=${target}&max_ttl=${max_ttl}&timeout=${timeout}`, worker, details)
}



function format_job_status_row(node)
{
    return `<tr> <td>${node.ttl}</td> <td>${node.ip}</td> <td>${node.country}</td> <td>${node.provider}</td> </tr>`
}


function compose_job_status(data)
{
    var title = `Tracing route to <i>${data.call_arguments.target}</i>.. (Max TTL: ${data.call_arguments.max_ttl}, Timeout: ${data.call_arguments.timeout} ms)`;
    document.getElementById('job_status_title').innerHTML = title;

    var table_content = format_job_status_row({
        'ttl': "<b>TTL</b>", 
        'ip': "<b>Address</b>", 
        'country': "<b>Country</b>",
        'provider': "<b>Autonomous System</b>"});
    for (var i = 0; i < data.nodes.length; i++) {
        table_content += format_job_status_row(data.nodes[i]);
    }

    document.getElementById('job_status_tbody').innerHTML = table_content;

    toggle_views(false);
}

function toggle_views(new_job=true)
{
    var x = document.getElementById("new_job_view");
    var y = document.getElementById("job_status_view");
    if (!new_job)
    {
        x.style.display = "none"; 
        y.style.display = "block";
    }
    else
    {
        x.style.display = "block"; 
        y.style.display = "none";
    }
}

function back_to_new_job()
{
    current_job = null;
    if (refresh_timer)
        clearInterval(refresh_timer);
    toggle_views();
}

function submit_new_job()
{
    var target = document.getElementById('new_job_target').value;
    var max_ttl = document.getElementById('new_job_max_ttl').value;
    var timeout = document.getElementById('new_job_timeout').value;

    current_job = null;

    submit_job(target, max_ttl, timeout,
        {"callback": (id) => 
            {
                refresh_timer = setInterval(() => {
                    get_state(id, {"callback": (data) => 
                    {
                        console.log("tick")
                        compose_job_status(data);
                        if (data.is_finished)
                            clearInterval(refresh_timer);
                    }  })
                }, 1000);
            } });
}


const form  = document.getElementById('new_job_form');
form.addEventListener('submit', (event) => {
    event.preventDefault();
    submit_new_job();
});
