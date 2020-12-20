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
                class="label-displayVal"
        >{{displayValue.toLocaleString(undefined, {maximumFractionDigits: 2})}}</p>
        <p
                class="label-min"
                :style="{left: `${percentMin * 100}%`}"
                v-show="showDetail"
        >{{targetMinValue}}</p>
        <p
                class="label-max"
                :style="{right: `${(1 - percentMax) * 100}%`}"
                v-show="showDetail"
        >{{targetMaxValue}}</p>
        <div class="bar" :class="{
            under: displayValue < targetMinValue,
            reached: displayValue >= targetMinValue && value <= targetMaxValue,
            over: displayValue > targetMaxValue}">
            <div class="value-portion" :style="{flexGrow: percentValue}"></div>
            <div class="proposed-portion" :style="{flexGrow: percentProposed}"></div>
            <div class="remaining-portion" :style="{flexGrow: percentRemaining}"></div>
            <div class="min-val-tick" :style="{left: `${percentMin * 100}%`, transform: percentMin >= 1 ? 'translateX(-200%)' : false}"></div>
            <div class="max-val-tick" :style="{left: `${percentMax * 100}%`, transform: 'translateX(-100%)'}"></div>
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
            },
            // A proposed relative amount (e.g. +2, -3, etc). If set, the value shown will be the value + proposedChange
            // and what proportions of the total value are the original value and proposed change will be made obvious
            // @todo support negative changes better
            proposedChange: {
                type: Number,
                default: null
            },
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
            // Determines the actual shown value, including any proposed change
            displayValue(){
                return this.value + (this.proposedChange || 0);
            },
            // Gets the largest value we consider, whether that's one of the targets, or the displayValue itself
            largestValue(){
                return Math.max(this.displayValue, this.targetMaxValue, this.targetMinValue)
            },
            percentValue() {
                return this.value / this.largestValue;
            },
            percentProposed() {
                return this.proposedChange / this.largestValue;
            },
            percentRemaining() {
                return 1 - (this.displayValue / this.largestValue);
            },
            percentMin(){
                return this.targetMinValue / this.largestValue;
            },
            percentMax(){
                return this.targetMaxValue / this.largestValue;
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
        --transition-speed: 0.5s;
        .bar {
            --bar-height: 3px;
            display: flex;
            position: relative;

            .value-portion {
                background: black;
                height: var(--bar-height);
                transition: all var(--transition-speed);
            }

            .proposed-portion {
                background: rgba(0, 0, 0, 0.5);
                height: var(--bar-height);
                transition: all var(--transition-speed);
            }

            .remaining-portion {
                height: 0;
                transition: all var(--transition-speed);
                align-self: center;
                border-top: 1px dashed #0002;
            }

            .min-val-tick, .max-val-tick {
                content: "";
                background-color: black;
                width: 1px;
                height: 1em;
                position: absolute;
                bottom: var(--bar-height);
                transition: all var(--transition-speed);
            }
            .max-val-tick{
                // We define the position from the left edge, but do not want to exceed outer edge of bar
                right: 0;
            }

            &.under{
                .value-portion{
                    background: rgb(124, 105, 0);
                }
                .proposed-portion{
                    background: rgba(124, 105, 0, 0.2);
                }
            }

            &.reached{
                .value-portion{
                    background: rgb(36, 123, 0);
                }
                .proposed-portion{
                    background: rgba(36, 123, 0, 0.5);
                }
            }

            &.over{
                .value-portion{
                    background: rgb(210, 0, 50);
                }
                .proposed-portion{
                    background: rgba(210, 0, 50, .5);
                }
            }
        }

        .label-displayVal{
            margin-left: 0.5em;
        }

        .label-min,
        .label-max{
            position: absolute;
            top: 0;
            font-size: 0.8em;
            padding: 0.2em;
            background: black;
            color: white;
            border-radius: var(--border-radius);
            transition: all var(--transition-speed);
        }
        .label-min{
            transform: translateX(calc(-100% - 0.5em));
        }
        .label-max{
            transform: translateX(-0.5em);
        }
    }
</style>