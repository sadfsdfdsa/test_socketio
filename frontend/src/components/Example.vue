<template>
    <b-container>
        <b-card>
            <b-row>
                <b-col>
                    <h3>This data comes from tarantool API</h3>
                    <p>Username: {{ testData.username }}</p>
                    <p>Password: {{ testData.password }}</p>
                    <p>Email: {{ testData.email }}</p>
                    <p>Created: {{ testData.tscreate | fdate }}</p>
                    <b-button
                        variant="primary"
                        @click="getTestData(2)"
                    >
                        Test Snotify
                    </b-button>
                </b-col>
                <router-link
                    :to="{name: 'indexPage'}"
                >
                    Back
                </router-link>
            </b-row>
        </b-card>
    </b-container>
</template>

<script>
export default {
    data: () => ({
        testData: []
    }),
    methods: {
        getTestData(id) {
            let body = {
                id: id || 1
            };

            this.$api.post("/example", body)
                .then(({data}) => {
                    if (data.result) {
                        this.testData = data.data;
                    } else {
                        this.$snotify.error(data.error)
                    }
                })
                .catch(e => {
                    this.$snotify.error(`Error status ${e.response.status}`);
                })
        }
    },
    filters: {
        fdate(ts) {
            if (!ts){
                return "Invalid Date"
            }

            let dateObj = (typeof(ts) === "string") ? new Date(ts) : new Date(ts * 1000);
            return dateObj.toLocaleString('en')
        }
    },
    created: function() {
        this.getTestData()
    }
}
</script>

<style>

</style>