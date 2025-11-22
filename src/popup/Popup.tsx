import { privateSearch } from "./api";

async function handleSearch() {
    const query = document.getElementById("searchInput").value;

    const result = await privateSearch(query);

    console.log("Sanitized results:", result);
    document.getElementById("output").textContent = JSON.stringify(result, null, 2);
}

document.getElementById("searchBtn").addEventListener("click", handleSearch);
