// get the json file that has our data
fetch("data.json")


    .then(function(response)
    {
        return response.json();
    })

    .then(function(data)
    {
        print("got here");
        // gets the section of the HTML site we wish to interact with
        let tbody = document.querySelector("#data-output");

        // let output = "";
        // for(let p of data)
        // {
        //     output += `
        //         <tr>
        //             <td> ${p.basin} </td>
        //             <td> ${p.river} </td>
        //             <td> ${p.flow} </td>
        //             <td> temp </td>
        //         </tr>
        //     `;
        // }
        // print(output);
        // tbody.append = output;

        // Iterate over JSON data and create table rows
        data.forEach(item => {
            // Create table row
            const row = document.createElement('tr');

            // Create table cells and populate them with data
            Object.values(item).forEach(value => {
                const cell = document.createElement('td');
                cell.textContent = value;
                row.appendChild(cell);
            });

            // Append row to table body
            tbody.appendChild(row);
        });
    })

    .catch(error => console.error('Error:', error));