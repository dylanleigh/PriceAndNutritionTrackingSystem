<!--
Target Summary

Component used to display a value in the context of a target range min and max value
-->
<template>
    <div
            :class="$options.name"
            :data-show-detail="showDetail"
            @click="forceDetail = !forceDetail"
            @mouseover="hovering = true"
            @mouseleave="hovering = false"
    >
        <p
                class="current-value"
        >{{value}}</p>
        <p
                class="min-value"
                :style="{left: `${percentMin * 100}%`}"
                v-show="showDetail"
        >{{targetMinValue}}</p>
        <p
                class="max-value"
                v-show="showDetail"
        >{{targetMaxValue}}</p>
        <div class="bar" :class="{
            under: value < targetMinValue,
            reached: value >= targetMinValue && value <= targetMaxValue,
            over: value > targetMaxValue}">
            <div class="value-portion" :style="{flexGrow: percentValue}"></div>
            <div class="remaining-portion" :style="{flexGrow: 1 - percentValue}"></div>
            <div class="min-val-tick" :style="{left: `${percentMin * 100}%`, transform: percentMin >= 1 ? 'translateX(-200%)' : false}"></div>
            <div class="max-val-tick"></div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "target-summary",
        props: {
            value: {
                type: Number,
                required: true
            },
            targetMinValue: {
                type: Number,
                required: true // @todo should the min and max be required? There is usually no min cost, and sometimes no max protein for ex.
            },
            targetMaxValue: {
                type: Number,
                required: true
            }
        },
        data() {
            return {
                // If true, the target value and other additional values will be shown
                forceDetail: false,
                // If the summary currently has the mouse over it
                hovering: false,
            }
        },
        computed: {
            percentValue() {
                return this.value / this.targetMaxValue;
            },
            percentMin(){
                return this.targetMinValue / this.targetMaxValue;
            },
            /**
             * Determines if greater detail should be shown for this component
             */
            showDetail(){
                return this.forceDetail || this.hovering;
            }
        }
    }
</script>

<style scoped lang="scss">
    .target-summary {
        position: relative;
        .bar {
            --bar-height: 3px;
            display: flex;
            position: relative;

            .value-portion {
                background: black;
                height: var(--bar-height);
            }

            .remaining-portion {
                background: rgba(0, 0, 0, 0.2);
                height: var(--bar-height);
            }

            .min-val-tick, .max-val-tick {
                content: "";
                background-color: black;
                width: 1px;
                height: 1em;
                position: absolute;
                bottom: var(--bar-height);
            }
            .max-val-tick{
                // We define the position from the left edge, but do not want to exceed outer edge of bar
                right: 0;
            }

            &.under{
                .value-portion{
                    background: red;
                }
                .remaining-portion{
                    background: rgba(255, 0, 0, 0.2);
                }
            }

            &.reached{
                .value-portion{
                    background: green;
                }
                .remaining-portion{
                    background: rgba(0, 255, 0, 0.2);
                }
            }

            &.over{
                .value-portion{
                    background: yellow;
                }
                .remaining-portion{
                    background: rgba(255, 255, 0, 0.2);
                }
            }
        }

        .current-value{
            margin-left: 0.5em;
        }

        .min-value,.max-value{
            position: absolute;
            top: 0;
            font-size: 0.8em;
            padding: 0.2em;
            background: black;
            color: white;
            border-radius: var(--border-radius);
        }
        .min-value{
            transform: translateX(calc(-100% - 0.5em));
        }
        .max-value{
            right: 0.5em;
        }
    }
</style>