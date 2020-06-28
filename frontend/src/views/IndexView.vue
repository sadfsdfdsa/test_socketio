<template>
    <div id="main">
        <b-container>
            <b-row class="mt-3" align-h="center">
                <b-col xl="6">
                    <b-card style="min-height: 500px; height: 500px;" class="bg-dark text-white">
                        <b-row v-for="(item, index) in this.infdata" v-bind:key="index">
                            <b-col sm="3" class="ins">
                                <strong>
                                    <ins v-if="author === item.author"> {{item.author}}:

                                    </ins>
                                    <span v-else>                                        {{item.author}}:

                                    </span>
                                </strong>
                            </b-col>
                            <b-col sm="6">{{item.msg}}</b-col>
                            <b-col sm="3"><i>
                                {{item.date.getHours()}}:{{item.date.getMinutes()}}:{{item.date.getSeconds()}}</i>
                            </b-col>
                        </b-row>
                    </b-card>
                </b-col>
            </b-row>
            <b-row class="mt-3" align-h="center">
                <b-col xl="5">
                    <b-input v-model="msg"></b-input>
                </b-col>
                <b-col xl="1">
                    <b-button @click="send_msg" :disabled="this.now_room===''" variant="success">Send</b-button>
                </b-col>
            </b-row>
            <b-row class="mt-3" align-h="center">
                <b-col xl="1">
                    Nickname:
                </b-col>
                <b-col xl="4">
                    <b-input v-model="author" class="bg-dark text-white"></b-input>
                </b-col>
            </b-row>
            <b-row class="mt-3" align-h="center">
                <b-col xl="1" v-for="(room, index) in this.rooms" v-bind:key="index">
                    <b-button @click="join_room(room)" :variant="room===now_room?'primary':'secondary'">{{room}}
                    </b-button>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import io from 'socket.io-client';


    export default {
        name: "IndexView",
        data: () => ({
            infdata: [],
            socket: null,
            msg: "",
            author: "Author",
            rooms: [],
            now_room: "",
            users: []
        }),
        methods: {
            init_sock() {
                // this.socket = io.connect('http://127.0.0.1:5000');
                this.socket = io.connect('https://chat-container.herokuapp.com:5000');
                this.socket.on("msg_client", (msgJson) => {
                    if (msgJson.msg) {
                        msgJson.date = new Date();
                        this.infdata.push(msgJson);
                    }
                });
                this.socket.on("system_event", (msg) => {
                    this.$snotify.warning(msg);
                });
                this.socket.on("room_users", (users) => {
                    this.users = users;
                });
            },
            send_msg() {
                this.socket.emit("msg_server", {msg: this.msg, author: this.author, room: this.now_room});
                this.msg = "";
            },
            join_room(room) {
                if (room !== this.now_room) {
                    if (this.now_room !== "") {
                        this.infdata = [];
                        this.socket.emit("leave_room", {room: this.now_room, user: this.author})
                    }
                    this.socket.emit("join_room", {room: room, user: this.author});
                    this.now_room = room;
                }
            }
        },
        created() {
            this.$api.get('/rooms/').then((data) => {
                this.rooms = data.data;
            })
            this.init_sock();
        }
    }
</script>

<style scoped>

</style>