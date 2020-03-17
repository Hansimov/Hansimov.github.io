
p5_property_list = [
    'width', 'height', 'windowWidth', 'windowHeight', 'frameCount',
    'noFill()', 'noStroke()',  'smooth()', 'noSmooth()',
    'push()', 'pop()', 'resetMatrix()',
    'preload()', 'setup()', 'draw()', 'loop()', 'noLoop()',
    'loadPixels()', 'updatePixels()'
    ]

p5_method_list = [
    'background', 'frameRate',
    'fill', 'stroke','strokeWeight', 'strokeCap', 'strokeJoin',
    'arc', 'ellipse', 'line', 'point', 'quad', 'rect', 'triangle',
    'colorMode', 'ellipseMode', 'rectMode', 'blendMode', 'imageMode',
    'bezier', 'curve', 
    'beginShape', 'endShape', 'vertex',
    'plane', 'box', 'sphere', 'cylinder', 'cone', 'ellipsoid', 'torus',
    'createCanvas', 'createGraphics',
    'applyMatrix', 'translate', 'rotate', 'scale', 'shearX', 'shearY',
    'loadImage', 'image', 
    'filter', 'blend',
    'textAlign', 'textLeading', 'textSize', 'textWidth', 'text',
    'textStyle',  'textAscent', 'textDescent', 'loadFont', 'textFont',
    'texture', 'shader', 'loadShader', 'createShader'
    ]


for p5prop in p5_property_list:
    with open('p5-' + p5prop + '.sublime-snippet','w') as spfile:
        spfile.write('<snippet>\n')
        spfile.write('<content><![CDATA[' + p5prop + ']]></content>\n') # Only difference
        spfile.write('<tabTrigger>' + p5prop + '</tabTrigger>\n')
        spfile.write('<scope>source.js</scope>\n')
        spfile.write('<description>p5: ' + p5prop + '</description>\n')
        spfile.write('</snippet>')

for p5method in p5_method_list:
    with open('p5-' + p5method + '.sublime-snippet','w') as spfile:
        spfile.write('<snippet>\n')
        spfile.write('<content><![CDATA[' + p5method + '($0)]]></content>\n') # Only difference
        spfile.write('<tabTrigger>' + p5method + '</tabTrigger>\n')
        spfile.write('<scope>source.js</scope>\n')
        spfile.write('<description>p5: ' + p5method + '(...)'+ '</description>\n')
        spfile.write('</snippet>')