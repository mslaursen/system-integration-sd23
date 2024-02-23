import express from 'express';

const app = express();

const PORT = 7070;
app.listen(PORT, () => console.log("Server is running on port", PORT));


app.get("/requestFastAPI", async (_, res) => {


    const url = "http://localhost:8080/fastapiData"
    
    const response = await fetch(url)

    const responseJson = await response.json()

    res.send(responseJson)
});


app.get("/expressData", (_, res) => {
    res.send({ data: "Data from express" })
}); 