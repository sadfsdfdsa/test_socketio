const axios = require("axios");

export default axios.create({
    baseURL: "/api/v1"
});

// you may add some more api callers and interceptors here
