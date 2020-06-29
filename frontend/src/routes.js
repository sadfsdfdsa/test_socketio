import IndexView from "./views/IndexView";
import GameView from "./views/GameView";


const routes = [
    {
        path: "/",
        component: IndexView,
        name: "indexPage",
        meta: {}
    },
        {
        path: "/game",
        component: GameView,
        name: "gamePage",
        meta: {}
    },
];

export default routes;