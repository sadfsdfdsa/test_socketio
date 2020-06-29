<template>
    <div id="main">
        <b-container>
            <b-row>
                <b-col sm="5" xl="2">
                    <b-input v-model="username" :disabled="username_disabled"></b-input>
                </b-col>
                <b-col sm="3" xl="3">
                    <b-button @click="save_name" variant="success" :disabled="username_disabled">Save name
                    </b-button>
                </b-col>
            </b-row>
            <section v-if="!start_game_flag">
                <b-card class="mt-3">
                    <section v-if="now_game.name===null" class="mb-3">
                        <b-row>
                            <b-col>
                                Create game:
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col sm="5" xl="2">
                                <b-input v-model="game_name_new"></b-input>
                            </b-col>
                            <b-col sm="3" xl="3">
                                <b-button @click="post_game" variant="primary" :disabled="!username_disabled">New game
                                </b-button>
                            </b-col>
                        </b-row>
                    </section>
                    <b-row>
                        <b-col>
                            Lobbies:
                            <span v-if="games.length===0"><i>No lobbies now</i></span>
                        </b-col>
                    </b-row>
                    <b-row class="mt-3">
                        <b-col v-for="game in this.games" v-bind:key="game.name" sm="2">
                                <b-button @click="join_game(game.name)"
                                          :disabled="!username_disabled || game.users.length>=2"
                                          :variant="game.name===now_game.name ? 'primary':'secondary'">
                                    {{game.name}}
                                    [{{game.users.length}}/2]
                                </b-button>
                        </b-col>
                    </b-row>
                </b-card>
            </section>
            <section v-if="this.now_game.name!==null" class="mt-3">
                <hr>
                <b-card>
                    <b-row>
                        <b-col xl="3" sm="8">
                            <h3>Lobby:
                                <ins>{{this.now_game.name}}</ins>
                                [{{this.now_game.users.length}}/2]
                            </h3>
                        </b-col>
                        <b-col>
                            <b-button @click="leave_game">Leave</b-button>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            Players: <i>{{this.now_game.users.join(', ')}}</i>
                        </b-col>
                    </b-row>
                </b-card>
                <section v-if="this.start_game_flag">
                    <b-row class="mt-3" no-gutters align-h="start">
                        <b-col>
                            <b-button-group>
                                <b-button @click="turn('камень')" variant="success" :disabled="now_game_state.turn"
                                          size="lg">Камень
                                </b-button>
                                <b-button @click="turn('ножницы')" variant="warning" :disabled="now_game_state.turn"
                                          size="lg">
                                    Ножницы
                                </b-button>
                                <b-button @click="turn('бумага')" variant="primary" :disabled="now_game_state.turn"
                                          size="lg">Бумага
                                </b-button>
                            </b-button-group>
                        </b-col>
                    </b-row>
                    <b-row class="mt-3">
                        <b-col>
                            <h4 class="text-primary">Your: {{now_game_state.value}}</h4>
                        </b-col>
                    </b-row>
                    <b-row class="mt-3">
                        <b-col>
                            <h4>Opponent's: {{now_game_state.opponent_value}}</h4>
                        </b-col>
                    </b-row>
                    <b-row class="mt-3">
                        <b-col>
                            <h3 :class="this.winner===this.username ? 'text-success' : 'text-danger'">Winner:
                                <ins>{{winner===username ? 'you' : winner}}</ins>
                            </h3>
                        </b-col>
                    </b-row>
                    <b-row class="mt-3">
                        <b-col>
                            History: <span v-for="(item, index) in this.history" v-bind:key="index"
                                           :class="item===username ? 'text-success' : 'text-danger'">{{item}}, </span>
                        </b-col>
                    </b-row>
                    <b-row v-if="winner!=='Ожидаем хода'">
                        <b-col>
                            <b-button :disabled="now_game_state.again_flag" @click="play_again">Play again
                                [{{now_game_state.again}}/2]
                            </b-button>
                        </b-col>
                    </b-row>
                </section>
            </section>
        </b-container>
    </div>
</template>

<script>
    import io from 'socket.io-client';


    export default {
        name: "IndexView",
        data: () => ({
            games: [],
            game_name_new: "",
            now_game: {
                name: null,
                users: []
            },
            now_game_state: {
                turn: false,
                value: null,
                opponent_value: null,
                again: 0,
                again_flag: false
            },
            history: [],
            winner: "Ожидаем хода",

            username: "ChangeYourName",
            username_disabled: false,
            start_game_flag: false
        }),
        methods: {
            init_sock() {
                this.socket = io.connect('http://127.0.0.1:5000');

                this.socket.on("new_game", (game) => {
                    this.games.push(game)
                });
                this.socket.on("delete_game", (game_name) => {
                    for (let i = 0; i < this.games.length; i++) {
                        if (this.games[i].name === game_name) {
                            this.$delete(this.games, i);
                        }
                    }
                });
                this.socket.on("join_user", (data) => {
                    for (let i = 0; i < this.games.length; i++) {
                        if (this.games[i].name === data.game) {
                            this.games[i].users.push(data.user)
                            if (this.games[i].name === this.now_game.name) {
                                this.now_game.users = this.games[i].users;
                            }
                            return;
                        }
                    }
                });
                this.socket.on("leave_user", (data) => {
                    for (let i = 0; i < this.games.length; i++) {
                        if (this.games[i].name === data.game) {
                            this.$delete(this.games[i].users, this.games[i].users.indexOf(data.user))
                            if (this.games[i].name === this.now_game.name) {
                                this.now_game.users = this.games[i].users;
                            }
                            return;
                        }
                    }
                });
                this.socket.on("start_game", () => {
                    this.start_game_flag = true;
                    this.now_game_state = {
                        turn: false,
                        value: null,
                        opponent_value: null,
                        again: 0,
                        again_flag: false
                    };
                    this.winner = "Ожидаем хода";
                });
                this.socket.on("unstart_game", () => {
                    this.start_game_flag = false;
                    this.now_game_state = {
                        turn: false,
                        value: null,
                        opponent_value: null
                    }
                    this.winner = "Ожидаем хода";
                });


                this.socket.on("end_turn", (data) => {
                    this.winner = data.winner;
                    this.history.push(this.winner);
                    this.now_game_state.opponent_value = data.turns[0].user === this.username ? data.turns[1].value : data.turns[0].value;
                });
                this.socket.on("add_play_again", () => {
                    this.now_game_state.again++;
                });


            },
            save_name() {
                this.username_disabled = true;
                localStorage.name = this.username;
            },
            post_game() {
                this.$api.post('/games/', {name: this.game_name_new}).then((data) => {
                    if (data.data.success === true) {
                        this.$snotify.success('Success');
                        this.join_game(this.game_name_new);
                        this.game_name_new = "";
                    } else {
                        this.$snotify.warning('Error');
                    }
                })
            },
            join_game(name) {
                if (this.now_game.name !== name) {
                    this.socket.emit('join_game', {'game': name, username: this.username});
                    if (this.now_game.name !== null) {
                        this.socket.emit('leave_game', {'game': this.now_game.name, username: this.username});
                        this.get_games();
                    }
                    this.history = [];
                    this.now_game.name = name;
                }
            },
            leave_game() {
                this.socket.emit('leave_game', {'game': this.now_game.name, username: this.username});
                this.now_game = {
                    name: null,
                    users: []
                };

                this.now_game_state = {
                    turn: false,
                    value: null,
                    opponent_value: null
                }
                this.winner = "Ожидаем хода";
                this.start_game_flag = false;
            },

            turn(value) {
                this.socket.emit('turn', {'game': this.now_game.name, username: this.username, turn: value});
                this.now_game_state.turn = true;
                this.now_game_state.value = value;
            },
            play_again() {
                this.now_game_state.again_flag = true;
                this.socket.emit("play_again", {game: this.now_game.name})
            },

            get_games() {
                this.$api.get('/games/').then((data) => {
                    this.games = data.data.games;
                })
            },

            getLS() {
                if (localStorage.getItem('name')) {
                    this.username = localStorage.getItem('name');
                    this.username_disabled = true;
                }
            }
        },
        created() {
            this.getLS();
            this.get_games();
            this.init_sock();
        },
        destroyed() {
            if (this.now_game.name !== null) {
                this.socket.emit('leave_game', {'game': this.now_game.name, username: this.username});
            }
        }
    }
</script>

<style scoped>

</style>