<script lang="ts">
    /**
     * I think Rasa went wrong by underestimating the growth of LLMs. Too much of their infrastructure is deterministic.
    */

import MsgBubble from "$lib/MsgBubble.svelte";

</script>
<h1>asar</h1>
<div class="msg-container">
    <MsgBubble msg="Hey there!" isUser={false}></MsgBubble>
    <MsgBubble msg="Do I know you?" isUser={true}></MsgBubble>
</div>

<style>
    .msg-container {
        background-color: lightblue;
        padding: 24px;
        width: 30vw;
        margin: auto;
        border-radius: 12px;
        box-shadow: 0px 0px 1px 0px;
    }
</style>