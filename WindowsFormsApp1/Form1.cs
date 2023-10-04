using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Text.Json;
using Newtonsoft.Json;
using System.Text.Json.Serialization;
using System.Net.Http;
using System.Net;
using System.Runtime.CompilerServices;
using System.Linq.Expressions;

namespace WindowsFormsApp1
{

    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
        PokemonArray pokeapi = new PokemonArray();

        private async void button1_Click(object sender, EventArgs e)
        {
            button1.Enabled = false;
            using (HttpClient client = new HttpClient())
            {
                try
                {
                    HttpResponseMessage response = await client.GetAsync("https://pokeapi.co/api/v2/pokemon/?limit=100000");
                    string json = await response.Content.ReadAsStringAsync();
                    pokeapi = JsonConvert.DeserializeObject<PokemonArray>(json);
                    List<Pokemon> list = pokeapi.Results.ToList();
                    foreach (var p in list)
                    {
                        listBox1.Items.Add(p.Name);
                    }    
                    
                }
                catch (Exception ex) { MessageBox.Show(ex.Message); }
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {

        }

        private async void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            var selected = pokeapi.Results.Where(p => p.Name == listBox1.SelectedItem.ToString());
            var items = selected.ToList()[0].Url.Split('/');
            pictureBox1.ImageLocation = $"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{items[items.Length - 2]}.png";
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            listBox1.Items.Clear();
            var array = pokeapi.Results.Where(p => p.Name.StartsWith(textBox1.Text)).ToArray();
            foreach (var pokemon in array)
            {
                listBox1.Items.Add(pokemon.Name);
            }
            if (textBox1.Text == "") 
            {
                List<Pokemon> list = pokeapi.Results.ToList();
                list.Sort();
                foreach (var p in list)
                {
                    listBox1.Items.Add(p.Name);
                }
            }
        }
    }
    class Pokemon: IComparable<Pokemon>
    {
        string name;
        public string Name { get; set; }
        public string Url { get; set; }
        public int CompareTo(Pokemon pokemon)
        {
            return string.Compare(this.Name, pokemon.Name);
        }
    }
    class PokemonArray
    {
        public Pokemon[] Results { get; set; }
    }
}
