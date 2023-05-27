



const SeasonalDemand = ({ dataSaeson }) => {

  const data = Object.keys(dataSaeson[0].fly_class).map((item) => {
    return {
      name: item,
      type: 'bar',
      x: dataSaeson.map((i) => i.date),
      y:dataSaeson.map((i)=>i.fly_class[item])

    }
  })

  console.log(data);
  return (
    <Plot
    data={data}
      layout={{
        width: '100%',
        barmode: 'stack'
      }}
    />
  )
}

export default SeasonalDemand