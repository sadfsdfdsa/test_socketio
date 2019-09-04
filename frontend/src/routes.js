import Example from "./components/Example.vue";
import Layout from "./components/Layout.vue";
import Index  from "./components/Index.vue";

import before from "./utils/before.js";

const routes = [
    {
        path: "/",
        component: Index,
        name: "indexPage",
        meta: {}
    },
    {
        path: "/authorized/",
        component: Layout,
        name: "examplePage",
        beforeEnter: before,
        meta: {},
        children: [
            {
                path: "example",
                component: Example,
                name: "examplePage",
                meta: {}
            }
            // authorized paths go here
        ]
    }
];

export default routes;