import express from "express";

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended:true }));

app.post("/githubwebhookjson", (req, res) => {
    console.log(req.body);
    res.status(204).send();
})

app.post("/githubwebhookform", (req, res) => {
    console.log(req.body)
    res.sendStatus(204)
});


app.get("/test", (_, res) => {
    res.send("Hello World!");
});

app.listen(8080, () => console.log("Server is running on port 8080"));