/*
* This is a connector for javascript to the PANTS api.
*/

/**
 * Encompassing class for the API, manages connecting to the remote resource and ferrying results back
 */
class Pants {
    /**
     *
     * @param api_hostname The hostname of the server
     * @param api_version The version of the api to use
     * @param api_uname The username to access the api with
     * @param api_pword The password to access the api with
     */
    constructor(api_hostname, api_version, api_uname, api_pword) {
        this.api_location = `http://${api_hostname}/api/${api_version}/`;
        this.api_uname = api_uname;
        this.api_pword = api_pword;
    }

    /**
     * Gets a fully qualified path to a specific api resource, given a relative path
     * @param relative_path The relative api path to access, e.g. 'ingredient/280'
     */
    get_api_path(relative_path){
        return this.api_location + relative_path
    }

    get_basic_auth_credentials() {
        return 'Basic ' + btoa(`${this.api_uname}:${this.api_pword}`)
    }

    /**
     * Gets a list of ingredients, supports searching, limit, offset, ordering
     *
     * @param {Object} options Options to pass to the api
     * @param {number} options.limit Maximum number of results to return
     * @param {number} options.offset Which ingredient to start returning results from
     * @param {string} options.ordering 
     *
     * @returns {Promise<void>}
     */
    async get_ingredients(options) {

        // Get the number of requested results
        let num_requested = options.endRow - options.startRow;

        let api_location = new URL(this.get_api_path('ingredient/'));
        api_location.searchParams.set('offset', options.startRow);
        api_location.searchParams.set('limit', num_requested);

        // Handle sorting options
        let ordering = [];
        for (let id of options.sortModel) {
            let param = '';
            param += id.sort === 'desc' ? '-' : '';
            param += id.colId;
            ordering.push(param)
        }
        api_location.searchParams.set('ordering', ordering.join(','));

        // Handle searching options
        api_location.searchParams.set('search', document.querySelector('#ingredient_filter').value);

        // Fetch the data
        let response = await fetch(api_location.toString(), {
            headers: new Headers({
                'Authorization': this.get_basic_auth_credentials()
            })
        });
        if (response.ok) {
            let data = await response.json();
            options.successCallback(data['results'], data['count'])
        } else {
            options.failCallback();
        }
    }

    /**
     * Reusable function for handling errors from the api
     */
    async handle_api_errors(response) {
        if (!response.ok) {
            throw Error(await response.text())
        }
        return response
    }

    /**
     * Updates an ingredient (identified by uri) based on the json object passed in
     * @param uri {string} The URI that uniquely identifies the given ingredient
     * @param json_details {Object} The details that will be overwritten onto the ingredient (details not included are unaffected)
     */
    async edit_ingredient(uri, json_details) {
        return fetch(uri, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': this.get_basic_auth_credentials()
            },
            body: JSON.stringify(json_details)
        })
            .then(this.handle_api_errors)
            .then(resp => resp.json())
            .catch(reason => alert(reason))
    }

    /**
     * Deletes the currently selected ingredient
     * @param ingredient_uri {string} The ingredient to delete
     */
    async delete_ingredient(ingredient_uri){
        // Send the command to delete the ingredient using the api
        return fetch(ingredient_uri, {
            method: 'DELETE',
            headers: {
                'Authorization': get_basic_auth_credentials()
            }
        })
        .then(this.handle_api_errors)
        .catch(reason => alert(reason))
    }

    /**
     * Creates a new ingredient using the information in the input fields
     * @param json_details {Object} The information for the ingredient
     */
    async create_ingredient(json_details){
        let form = document.querySelector('#ingredient_edit_form');
        let tags = form.querySelector('[name=tags]').value.split(',');
        // Remove empty tags
        tags = tags.filter(tag => tag !== '');

        return fetch(this.get_api_path('ingredient/'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': this.get_basic_auth_credentials()
            },
            body: JSON.stringify(json_details)
        })
            .then(this.handle_api_errors)
            .then(resp => resp.json())
            .catch(reason => alert(reason))
    }


}

