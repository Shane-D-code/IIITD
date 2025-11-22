export async function privateSearch(query) {
    const response = await fetch("https://didactic-lamp-jjp944vx9xqpfpxx5-3000.app.github.dev/debug", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query })
    });

    return response.json();
}
