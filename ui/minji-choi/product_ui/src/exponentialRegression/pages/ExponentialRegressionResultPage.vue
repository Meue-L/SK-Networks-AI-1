<template>
    <v-container class="chart-container">
        <h2>Exponential Regression Chart</h2>
        <v-row>
            <v-col>
                <div ref="chart"></div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import * as d3 from 'd3'
import {ref, onMounted} from 'vue'


export default {
    setup () {
        const chart = ref(null)
        const originalData = ref([])
        const predictedData = ref([])
        const fetchExponentialRegressionData = async () => {
            try {
                const response = await fetch('http://127.0.0.1:33333/exponential-regression')
                const data = await response.json()
                originalData.value = data.original_data
                console.log('originalData : ', originalData.value)
                predictedData.value = data.predicted_data
                console.log('predictedData : ', predictedData)

            } catch (error) {
                console.error('exponential 회귀 분석 데이터 확보 중 에러 발생', error)
            }
        }
        const drawChart = () => {
            const margin = {top:20, right: 20, bottom: 30, left:40}
            const width = 960 - margin.left - margin.right
            const height = 500 - margin.top - margin.bottom

            const x = d3.scaleLinear().range([0, width])
            const y = d3.scaleLinear().range([height, 0])

            const line = d3.line()
                            .x(d => x(d[0]))
                            .y(d => y(d[1]))

            const svg = d3.select(chart.value).append('svg')
                                .attr('width', width + margin.left + margin.right)
                                .attr('height', height + margin.top + margin.bottom)
                                .append('g')
                                .attr('transform', `translate(${margin.left}, ${margin.top})`)
            x.domain(d3.extent(originalData.value, d => d[0]))
            y.domain([0, d3.max(originalData.value, d => d[1])])

            svg.append('g')
                    .attr('class', 'x axis')
                    .attr('transform', `translate(0, ${height})`)
                    .call(d3.axisBottom(x))
            svg.append('g')
                    .attr('calss', 'y axis')
                    .call(d3.axisLeft(y))

            svg.append('path')
                    .datum(originalData.value)
                    .attr('class','line')
                    .attr('d',line)
                    .style('stroke','steelblue')
                    .style('fill','none') // 검정색으로 채워지지 않도록!!!

            svg.append('path')
                    .datum(predictedData.value)
                    .attr('class','line')
                    .attr('d',line)
                    .style('stroke','red')
                    .style('fill','none')

            // svg.selectAll('.dot')
            //         .data(originalData.value)
            //         .enter().append('circle')
            //         .attr('class','dot')
            //         .attr('cx', d => x(d[0]))
            //         .attr('cy', d => y(d[1]))
            //         .attr('r',3)
            //         .style('fill','steelblue') // 동그라미로 보기 위해 추가? 하는 것
                }
        onMounted (async () => {
            await fetchExponentialRegressionData()
            drawChart()
        })
        // 원래 데이터 설정할 떄 data () {return : { chart}}
        // 대략 위와 같은 느낌이었음
        // 그러나 setup() 내에서 사용할 때 data를 직접 표기하지 않고 return에 배치해서
        // 데이터나 refs를 맵핑한다 보면 됨
        return {chart}
    }
}
</script>