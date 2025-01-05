document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("#discount-table tbody");
    const spinner = document.getElementById("spinner");
    const addButton = document.getElementById("add-button");
    const modal = document.getElementById("add-item-modal");
    const closeModal = document.getElementById("close-modal");
    const itemSearch = document.getElementById("item-search");
    const searchResults = document.getElementById("search-results");

    function showSpinner() {
        spinner.style.display = "block";
    }

    function hideSpinner() {
        spinner.style.display = "none";
    }

    function populateTable(data) {
        tableBody.innerHTML = "";
        const c_data = data.c_data;
        const ww_data = data.ww_data;
        c_data.forEach((colRow, i) => {
            const wwRow = ww_data[i];
            const row = document.createElement("tr");

            const productCell = document.createElement("td");
            productCell.textContent = colRow[2];
            row.appendChild(productCell);

            const colesCell = document.createElement("td");
            colesCell.textContent = colRow[3];
            if (colRow[1]) colesCell.classList.add("bold-yellow");
            colesCell.classList.add("align-right");
            row.appendChild(colesCell);

            const wooliesCell = document.createElement("td");
            wooliesCell.textContent = wwRow[3];
            if (wwRow[1]) wooliesCell.classList.add("bold-yellow");
            wooliesCell.classList.add("align-right");
            row.appendChild(wooliesCell);

            tableBody.appendChild(row);
        });
    }

    function fetchData() {
        showSpinner();
        fetch('/data')
            .then(response => response.json())
            .then(data => {
                populateTable(data);
                hideSpinner();
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                hideSpinner();
            });
    }

    // Open modal
    addButton.addEventListener("click", () => {
        modal.style.display = "flex";
    });

    // Close modal
    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // Search for items
    itemSearch.addEventListener("input", () => {
        const query = itemSearch.value;
        if (query.length > 0) {
            fetch(`/search?query=${query}`)
                .then(response => response.json())
                .then(data => {
                    searchResults.innerHTML = "";
                    data.forEach(item => {
                        const li = document.createElement("li");
                        li.textContent = item.name;
                        li.addEventListener("click", () => {
                            addItemToList(item.id);
                        });
                        searchResults.appendChild(li);
                    });
                })
                .catch(error => console.error("Error fetching search results:", error));
        } else {
            searchResults.innerHTML = ""; // Clear results if input is empty
        }
    });

    // Add item to the list
    function addItemToList(itemId) {
        fetch(`/add-item`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ id: itemId }),
        })
            .then(response => response.json())
            .then(() => {
                modal.style.display = "none";
                fetchData();
            })
            .catch(error => console.error("Error adding item:", error));
    }

    fetchData(); // Initial data fetch
});