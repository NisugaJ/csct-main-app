function getSimpleDateTime(){

    return (new Date()).toISOString().toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    }).replace(/,|\s/g, '-')
}

export default getSimpleDateTime