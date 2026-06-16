import { useRouter } from "vue-router";
import { ClipboardList, CalendarPlus, Camera } from "lucide-vue-next";

export default {
    name: "MainMenu",
    components: {
        ClipboardList,
        CalendarPlus,
        Camera,
    },
    setup() {
        const router = useRouter();

        const goTo = (path) => {
            router.push(path);
        };

        return {
            goTo,
        };
    },
};
