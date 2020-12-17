<!--
Target Summary

Component used to display a value in the context of a target range min and max value
-->
<template>
    <div
            :class="$options.name"
            :data-show-detail="showDetail"
            @click="showDetail = !showDetail"
    >
        <p>{{value}}</p>
        <p
                class="min-value"
                :style="{left: `${percentMin * 100}%`}"
                v-show="showDetail"
        >{{targetMinValue}}</p>
        <p
                class="max-value"
                v-show="showDetail"
        >{{targetMaxValue}}</p>
        <div class="bar" :class="{under: value < targetMinValue, reached: value >= targetMinValue && value <= targetMaxValue, over: value > targetMaxValue}">
            <div class="value-portion" :style="{flexGrow: percentValue}"></div>
            <div class="remaining-portion" :style="{flexGrow: 1 - percentValue}"></div>
            <div class="min-val-tick" :style="{left: `${percentMin * 100}%`}"></div>
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
                showDetail: false
            }
        },
        computed: {
            percentValue() {
                return this.value / this.targetMaxValue;
            },
            percentMin(){
                return this.targetMinValue / this.targetMaxValue;
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
                height: calc(var(--bar-height) + 1em);
                position: absolute;
                bottom: 0;
            }
            .max-val-tick{
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

        .min-value,.max-value{
            position: absolute;
            top: 0;
        }
        .min-value{
            transform: translateX(calc(-100% - 0.5em));
        }
        .max-value{
            right: 0.5em;
        }
    }
</style>