// get the json file that has our data
fetch("data.json")


.then(function(response)
{
    return response.json();
})

.then(function(products)
{
    // gets the section of the HTML site we wish to interact with
    let placeholder = document.querySelector("#data-output");

    let output = "";
    for(let p of products)
    {
        output += `
            <tr>
                <td> ${p.basin} </td>
                <td> ${p.river} </td>
                <td> ${p.flow} </td>
                <td> temp </td>
            </tr>
        `;
    }

    placeholder.innerHTML = output;
})