<script lang="ts">
    export let msg: string;
    export let isUser: boolean;

    const userColor = "#0088ff";
    const otherColor = "#999";
</script>

<div class="bubble-div-outer">
    <div class="msg-bubble" style="--bubble-color: {isUser ? userColor : otherColor}; --float-dir: {isUser ? 'right' : 'left'};">{msg}</div>
</div>

<style>
    .bubble-div-outer {
        display: inline-block;
        width: 100%;
    }

    .msg-bubble {
        float: var(--float-dir);
        animation-name: bubble-appear;
        animation-duration: 0.2;
        background-color: var(--bubble-color);
        border-radius: 12px;
        padding: 6px;
        color: white;
    }

    @keyframes bubble-appear {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
</style>