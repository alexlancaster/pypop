<!--
This file is part of PyPop

  Copyright (C) 2003, 2004. The Regents of the University of California
  (Regents)  All Rights Reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
USA.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF
ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION
TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS.
-->
<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exsl="http://exslt.org/common"
 xmlns:str="http://exslt.org/strings"
 xmlns:set="http://exslt.org/sets"
 extension-element-prefixes="exsl str set"
 xmlns:data="any-uri">

 <xsl:import href="lib.xsl"/>

 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes" indent="no" encoding="UTF-8"/>

 <!-- specify a default directory for the output .tsv files that can be overriden -->
 <xsl:param name="outputDir" select="'./'"/>

 <!-- specify a default prefix for all .tsv files that can be overriden -->
 <xsl:param name="prefixTSV" select="''"/>

 <!-- generate overall file prefix -->
 <xsl:variable name="filePrefix">
   <xsl:value-of select="$outputDir"/><xsl:value-of select="$prefixTSV"/>
 </xsl:variable>
 
 <xsl:param name="output.genotype.distrib" select="0"/>

 <data:map-order>
  <locusname order="1">D6S2239</locusname>
  <locusname order="2">D6S2223</locusname>
  <locusname order="3">D6S2222</locusname>
  <locusname order="4">A</locusname>
  <locusname order="5">D6S265</locusname>
  <locusname order="6">C</locusname>
  <locusname order="7">B</locusname>
  <locusname order="8">MIB</locusname>
  <locusname order="9">TNFD</locusname>
  <locusname order="10">D6S273</locusname>
  <locusname order="11">DRA</locusname>
  <locusname order="12">DRB1</locusname>
  <locusname order="13">DRB3</locusname>
  <locusname order="14">DQA1</locusname>
  <locusname order="15">DQIV</locusname>
  <locusname order="16">DQCARII</locusname>
  <locusname order="17">DQCAR</locusname>
  <locusname order="18">DQB1</locusname>
  <locusname order="19">G51152</locusname>
  <locusname order="20">DPA1</locusname>
  <locusname order="21">DPB1</locusname>
  <locusname order="22">D6S291</locusname>
 </data:map-order>

 <data:region-order>
  <regionname long="Sub-Saharan-Africa">01.SS-Africa</regionname>
  <regionname long="North-Africa">02.N-Africa</regionname>	  
  <regionname long="Europe">03.Europe</regionname>	  
  <regionname long="South-West-Asia">04.SW-Asia</regionname>	  
  <regionname long="South-East-Asia">05.SE-Asia</regionname>	  
  <regionname long="Oceania">06.Oceania</regionname>	  
  <regionname long="Australia">07.Australia</regionname>	  
  <regionname long="North-East-Asia">08.NE-Asia</regionname>	  
  <regionname long="North-America">09.N-America</regionname>	  
  <regionname long="South-America">10.S-America</regionname>	  
  <regionname long="Other">11.Other</regionname>          
 </data:region-order>

 <xsl:param name="ihwg-fmt" select="0"/>

 <xsl:param name="map-order" 
  select="document('')//data:map-order/locusname"/>

 <xsl:param name="region-order" 
  select="document('')//data:region-order/regionname"/>

 <xsl:param name="ihwg-header-line-start">pop&#09;labcode&#09;method&#09;ethnic&#09;collect.site&#09;region&#09;latit&#09;longit&#09;complex&#09;</xsl:param>

 <xsl:template name="header-line-start">
  <xsl:param name="popnode"/>
  <xsl:choose>
   <xsl:when test="$ihwg-fmt">
    <xsl:value-of select="$ihwg-header-line-start"/>
   </xsl:when>
   <xsl:otherwise>
    <xsl:for-each select="$popnode/*">
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="name(.)"/>
     </xsl:call-template>
    </xsl:for-each>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <xsl:template name="output-field">
  <xsl:param name="node"/>

  <xsl:choose>
   <!-- if the node exists and is non-empty print it's value -->
   <xsl:when test="$node and not($node='')">
    <xsl:value-of select="$node"/>
   </xsl:when>
   <!-- otherwise output placeholder -->
   <xsl:otherwise>****</xsl:otherwise>
  </xsl:choose>

  <!-- output tab -->
  <xsl:text>&#09;</xsl:text>
  
 </xsl:template>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>
 
 <xsl:template name="line-start">
  <xsl:param name="popnode"/>

  <xsl:choose>
   <xsl:when test="$ihwg-fmt">

    <xsl:call-template name="output-field">
     <xsl:with-param name="node">
      <xsl:choose>
       <xsl:when test="$popnode/popname">
	<xsl:value-of select="translate($popnode/popname, ' ', '-')"/>
       </xsl:when>
       <xsl:otherwise>
	<xsl:value-of select="substring-before($popnode/../filename, '.')"/>
       </xsl:otherwise>
      </xsl:choose>
     </xsl:with-param>
    </xsl:call-template>
    
    <xsl:call-template name="output-field">
     <xsl:with-param name="node" select="translate($popnode/labcode, ' ', '-')"/>
    </xsl:call-template>
    
    <xsl:call-template name="output-field">
     <xsl:with-param name="node" select="translate($popnode/method, ' ', '-')"/>
    </xsl:call-template>
    
    <xsl:call-template name="output-field">
     <xsl:with-param name="node" select="translate($popnode/ethnic, ' ', '-')"/>
    </xsl:call-template>

    <xsl:call-template name="output-field">
     <xsl:with-param name="node" select="translate($popnode/collect, ' ', '-')"/>
    </xsl:call-template>
    
    <!-- apply short form of regions as defined in lookup table -->
    <xsl:call-template name="output-field">
     <xsl:with-param name="node" select="$region-order[@long=translate($popnode/contin, ' ', '-')]"/>
    </xsl:call-template>
    
    <xsl:call-template name="output-field">
     <xsl:with-param name="node" select="translate($popnode/latit, ' ', '_')"/>
    </xsl:call-template>
    
    <xsl:call-template name="output-field">
     <xsl:with-param name="node" select="translate($popnode/longit, ' ', '_')"/>
    </xsl:call-template>
    
    <xsl:call-template name="output-field">
     <xsl:with-param name="node" select="translate($popnode/complex, ' ', '_')"/>
    </xsl:call-template>
    
   </xsl:when>
   <xsl:otherwise>
    <xsl:for-each select="$popnode/*">
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="."/>
     </xsl:call-template>
    </xsl:for-each>
   </xsl:otherwise>  
  </xsl:choose>
 </xsl:template>

 <xsl:template name="gen-lines">
  <xsl:param name="nodes"/>
  <xsl:param name="type" select="'1'"/>
  <xsl:param name="pairwise" select="1"/>

  <xsl:for-each select="$nodes">

   <xsl:choose>

    <xsl:when test="$type='1-locus-hardyweinberg'">

     <xsl:variable name="cur-node" select="."/>

     <!-- get the unique lump levels for all HW tests -->
     <xsl:variable name="unique-lump-levels">
      <xsl:for-each select="*//@allelelump">
       <xsl:variable name="cur-lump" select="."/>
       <xsl:if test="not($cur-lump = preceding)">
	<unique><xsl:value-of select="."/></unique>
       </xsl:if>
      </xsl:for-each>
     </xsl:variable>
     
     <xsl:variable name="lump-levels" select="set:distinct(*//@allelelump)"/>

     <!--
      <xsl:message>
      <xsl:for-each select="$lump-levels">
       <xsl:value-of select="."/>
       <xsl:call-template name="newline"/>
      </xsl:for-each>
      </xsl:message>
     -->

     <xsl:for-each select="$lump-levels">
      
      <xsl:variable name="lump" select="."/>

      <xsl:call-template name="line-start">
       <xsl:with-param name="popnode" select="$cur-node/../populationdata"/>
      </xsl:call-template>
      
      <xsl:call-template name="output-field">
       <xsl:with-param name="node">
	<xsl:value-of select="translate($cur-node/@name, '*', '')"/>
       </xsl:with-param>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node">
	<xsl:value-of select="$lump"/>
       </xsl:with-param>
      </xsl:call-template>
      
      <xsl:variable name="hwGT" select="$cur-node/hardyweinbergGuoThompson[@allelelump=$lump]"/>
      <xsl:variable name="hwGT-alleles" 
       select="count(set:distinct($hwGT/genotypetable/genotype/@col))"/>

      <xsl:variable name="hw" 
       select="$cur-node/hardyweinberg[@allelelump=$lump]"/>

      <xsl:variable name="hw-alleles" 
       select="count(set:distinct($hw/genotypetable/genotype/@col))"/>
      
      <xsl:variable name="hwEnum" select="$cur-node/hardyweinbergEnumeration[@allelelump=$lump]"/>

      <xsl:variable name="hwEnum-alleles" 
       select="count(set:distinct($hwEnum/genotypetable/genotype/@col))"/>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node">
	<xsl:choose>
	 <xsl:when test="$hw-alleles &gt; 0">
	  <xsl:value-of select="$hw-alleles"/>
	 </xsl:when>
	 <xsl:when test="$hwGT-alleles &gt; 0">
	  <xsl:value-of select="$hwGT-alleles"/>
	 </xsl:when>
	 <xsl:when test="$hwEnum-alleles &gt; 0">
	  <xsl:value-of select="$hwEnum-alleles"/>
	 </xsl:when>
	 <xsl:otherwise>
	  <xsl:text>****</xsl:text>
	 </xsl:otherwise>
	</xsl:choose>
       </xsl:with-param>
      </xsl:call-template>


      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$hwGT[not(@type='monte-carlo')]/pvalue[@type='overall']"/>
      </xsl:call-template>
      
      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$hwGT[@type='monte-carlo']/pvalue[@type='overall']"/>
      </xsl:call-template>
      
      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$hwEnum/pvalue[@type='overall']"/>
      </xsl:call-template>
      
      <xsl:choose>
       <!--complete -->
       <xsl:when
	test="$hw/lumped/@role='no-rare-genotypes' and 
	hardyweinberg/common!=''">
	<xsl:value-of select="$hw/common/pvalue"/>
       </xsl:when>
       <!-- common + lumped -->
       <xsl:when test="$hw/lumped!='' and 
	$cur-node/hardyweinberg/common!=''">
	<xsl:value-of select="$hw/common/pvalue"/>
       </xsl:when>
       <!-- common -->
       <xsl:when test="$hw/common!=''">
	<xsl:value-of select="$hw/common/pvalue"/>
       </xsl:when>

      <!-- if either no-common-genotypes or too-many-parameters is found -->
      <!-- output the role attribute rather than a N/A '****' -->
      <!-- make sure that this node actually has data -->
      <!-- should be fixed properly by outputing <hardyweinberg> with a -->
      <!-- role="no-data" attribute -->
      <xsl:when test="$hw/common[@role='no-common-genotypes' or @role='too-many-parameters'] and $hw/samplesize!=0">
       <xsl:value-of select="$hw/common/@role"/>
      </xsl:when>

      <xsl:otherwise>****</xsl:otherwise>
     </xsl:choose>
     <xsl:text>&#09;</xsl:text>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="$hw/homozygotes/pvalue"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="$hw/heterozygotes/pvalue"/>
     </xsl:call-template>

      <xsl:variable name="hwGTA" select="$cur-node/hardyweinbergGuoThompsonArlequin"/>

     <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$hwGTA/pvalue"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="$hwGTA/stddev"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="$hwGTA/exp-hetero"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="$hwGTA/obs-hetero"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node">
       <xsl:choose>
	<xsl:when test="$hw/samplesize='0'">
	 <xsl:value-of select="'****'"/>
	</xsl:when>
	<xsl:otherwise>
	 <xsl:value-of select="count($hw/genotypetable/genotype[not(chisq/@role='not-calculated')])"/>
	</xsl:otherwise>
       </xsl:choose>
      </xsl:with-param>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node">
       <xsl:choose>
	<xsl:when test="$hw/samplesize='0'">
	 <xsl:value-of select="'****'"/>
	</xsl:when>
	<xsl:otherwise>
	 <xsl:value-of select="count($hw/genotypetable/genotype/pvalue[. &lt;= 0.05])"/>
	</xsl:otherwise>
       </xsl:choose>
      </xsl:with-param>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node">
       <xsl:choose>
	<xsl:when test="$hw/samplesize='0'">
	 <xsl:value-of select="'****'"/>
	</xsl:when>
	<xsl:otherwise>
	 <xsl:value-of select="count($hw/heterozygotesByAllele/allele)"/>
	</xsl:otherwise>
       </xsl:choose>
      </xsl:with-param>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node">
       <xsl:choose>
	<xsl:when test="$hw/samplesize='0'">
	 <xsl:value-of select="'****'"/>
	</xsl:when>
	<xsl:otherwise>
	 <xsl:value-of select="count($hw/heterozygotesByAllele/allele/pvalue[. &lt;= 0.05])"/>
	</xsl:otherwise>
       </xsl:choose>
      </xsl:with-param>
     </xsl:call-template>

      <xsl:call-template name="newline"/>
     </xsl:for-each>
     
    </xsl:when>

    <xsl:when test="$type='1-locus-summary'">

     <xsl:call-template name="line-start">
      <xsl:with-param name="popnode" select="../populationdata"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="translate(@name, '*', '')"/>
     </xsl:call-template>

     <xsl:choose>
      <xsl:when test="allelecounts/allelecount">
       <xsl:value-of select="allelecounts/allelecount"/>
      </xsl:when>
      <xsl:otherwise>0</xsl:otherwise>
     </xsl:choose>
     <xsl:text>&#09;</xsl:text>

     <xsl:choose>
      <xsl:when test="allelecounts/untypedindividuals">
       <xsl:value-of select="allelecounts/untypedindividuals"/>
      </xsl:when>
      <xsl:otherwise>0</xsl:otherwise>
     </xsl:choose>
     <xsl:text>&#09;</xsl:text>

     <xsl:choose>
      <xsl:when test="allelecounts/unsequencedsites">
       <xsl:value-of select="allelecounts/unsequencedsites"/>
      </xsl:when>
      <xsl:otherwise>0</xsl:otherwise>
     </xsl:choose>
     <xsl:text>&#09;</xsl:text>

     <xsl:choose>
      <xsl:when test="allelecounts/distinctalleles">
       <xsl:value-of select="allelecounts/distinctalleles"/>
      </xsl:when>
      <xsl:otherwise>0</xsl:otherwise>
     </xsl:choose>
     <xsl:text>&#09;</xsl:text>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosity/pvalue/lower"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosity/pvalue/upper"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosity/normdev"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="hardyweinbergGuoThompson[not(@type='monte-carlo')]/pvalue[@type='overall']"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="hardyweinbergGuoThompson[@type='monte-carlo']/pvalue[@type='overall']"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="hardyweinbergEnumeration/pvalue[@type='overall']"/>
     </xsl:call-template>

     
     <xsl:choose>
      <!--complete -->
      <xsl:when
       test="hardyweinberg/lumped/@role='no-rare-genotypes' and 
       hardyweinberg/common!=''">
       <xsl:value-of select="hardyweinberg/common/pvalue"/>
      </xsl:when>
      <!-- common + lumped -->
      <xsl:when test="hardyweinberg/lumped!='' and 
       hardyweinberg/common!=''">
       <xsl:value-of select="hardyweinberg/common/pvalue"/>
      </xsl:when>
      <!-- common -->
      <xsl:when test="hardyweinberg/common!=''">
       <xsl:value-of select="hardyweinberg/common/pvalue"/>
      </xsl:when>

      <!-- if either no-common-genotypes or too-many-parameters is found -->
      <!-- output the role attribute rather than a N/A '****' -->
      <!-- make sure that this node actually has data -->
      <!-- should be fixed properly by outputing <hardyweinberg> with a -->
      <!-- role="no-data" attribute -->
      <xsl:when test="hardyweinberg/common[@role='no-common-genotypes' or @role='too-many-parameters'] and hardyweinberg/samplesize!=0">
       <xsl:value-of select="hardyweinberg/common/@role"/>
      </xsl:when>

      <xsl:otherwise>****</xsl:otherwise>
     </xsl:choose>
     <xsl:text>&#09;</xsl:text>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="hardyweinberg/homozygotes/pvalue"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="hardyweinberg/heterozygotes/pvalue"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="hardyweinbergGuoThompsonArlequin/pvalue"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="hardyweinbergGuoThompsonArlequin/stddev"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="hardyweinbergGuoThompsonArlequin/exp-hetero"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="hardyweinbergGuoThompsonArlequin/obs-hetero"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosityEWSlatkinExact/observedHomozygosity"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosityEWSlatkinExact/meanHomozygosity"/>
     </xsl:call-template>
    
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosityEWSlatkinExact/normDevHomozygosity"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosityEWSlatkinExact/probHomozygosity"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosityEWSlatkinExact/varHomozygosity"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosityEWSlatkinExact/probEwens"/>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node">
       <xsl:choose>
	<xsl:when test="hardyweinberg/samplesize='0'">
	 <xsl:value-of select="'****'"/>
	</xsl:when>
	<xsl:otherwise>
	 <xsl:value-of select="count(hardyweinberg/genotypetable/genotype[not(chisq/@role='not-calculated')])"/>
	</xsl:otherwise>
       </xsl:choose>
      </xsl:with-param>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node">
       <xsl:choose>
	<xsl:when test="hardyweinberg/samplesize='0'">
	 <xsl:value-of select="'****'"/>
	</xsl:when>
	<xsl:otherwise>
	 <xsl:value-of select="count(hardyweinberg/genotypetable/genotype/pvalue[. &lt;= 0.05])"/>
	</xsl:otherwise>
       </xsl:choose>
      </xsl:with-param>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node">
       <xsl:choose>
	<xsl:when test="hardyweinberg/samplesize='0'">
	 <xsl:value-of select="'****'"/>
	</xsl:when>
	<xsl:otherwise>
	 <xsl:value-of select="count(hardyweinberg/heterozygotesByAllele/allele)"/>
	</xsl:otherwise>
       </xsl:choose>
      </xsl:with-param>
     </xsl:call-template>

     <xsl:call-template name="output-field">
      <xsl:with-param name="node">
       <xsl:choose>
	<xsl:when test="hardyweinberg/samplesize='0'">
	 <xsl:value-of select="'****'"/>
	</xsl:when>
	<xsl:otherwise>
	 <xsl:value-of select="count(hardyweinberg/heterozygotesByAllele/allele/pvalue[. &lt;= 0.05])"/>
	</xsl:otherwise>
       </xsl:choose>
      </xsl:with-param>
     </xsl:call-template>

     
     <xsl:call-template name="newline"/>

    </xsl:when>

    <xsl:when test="$type='1-locus-allele'">

     <xsl:variable name="curr-line-start">
      <xsl:call-template name="line-start">
       <xsl:with-param name="popnode" select="../populationdata"/>
      </xsl:call-template>
     </xsl:variable>

     <xsl:for-each select="allelecounts/allele">
      <xsl:value-of select="$curr-line-start"/>

      <xsl:value-of select="../../@name"/>
      <xsl:text>&#09;</xsl:text>

      <xsl:value-of select="@name"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:value-of select="frequency"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:value-of select="count"/>
      <xsl:call-template name="newline"/>
     </xsl:for-each>
    </xsl:when>

    <xsl:when test="$type='1-locus-genotype'">

     <xsl:variable name="curr-line-start">
      <xsl:call-template name="line-start">
       <xsl:with-param name="popnode" select="../populationdata"/>
      </xsl:call-template>
     </xsl:variable>

     <xsl:variable name="pvals-chen-mcmc"
     select="hardyweinbergGuoThompson[not(@type='monte-carlo')]/pvalue[@statistic='chen_statistic' and @type='genotype']"/>

     <xsl:variable name="pvals-chen-monte-carlo" select="hardyweinbergGuoThompson[@type='monte-carlo']/pvalue[@statistic='chen_statistic' and @type='genotype']"/>

     <xsl:variable name="pvals-diff-mcmc"
     select="hardyweinbergGuoThompson[not(@type='monte-carlo')]/pvalue[@statistic='diff_statistic' and @type='genotype']"/>

     <xsl:variable name="pvals-diff-monte-carlo" select="hardyweinbergGuoThompson[@type='monte-carlo']/pvalue[@statistic='diff_statistic' and @type='genotype']"/>

     <xsl:variable name="pvals-diff-enum" select="hardyweinbergEnumeration/pvalue[@statistic='diff_statistic' and @type='genotype']"/>

     <xsl:variable name="pvals-chen-enum" select="hardyweinbergEnumeration/pvalue[@statistic='chen_statistic' and @type='genotype']"/>

     <xsl:variable name="pvals-diff-enum-3x3" select="hardyweinbergEnumeration/pvalue[@statistic='diff_statistic_3x3' and @type='genotype']"/>

     <xsl:variable name="pvals-chen-enum-3x3" select="hardyweinbergEnumeration/pvalue[@statistic='chen_statistic_3x3' and @type='genotype']"/>

     <!-- get the number of steps in both mcmc and mc version -->
     <xsl:variable name="steps-mcmc"
     select="hardyweinbergGuoThompson[not(@type='monte-carlo')]/samplingNum * hardyweinbergGuoThompson[not(@type='monte-carlo')]/samplingSize"/>

     <xsl:variable name="steps-monte-carlo" select="hardyweinbergGuoThompson[@type='monte-carlo']/steps"/>
     
     <!-- get actual test statistics -->
     <xsl:variable name="stats-chen-monte-carlo" select="hardyweinbergGuoThompson[@type='monte-carlo']/genotypeSimulatedStatistic[@statistic='chen_statistic']"/>

     <xsl:variable name="stats-diff-monte-carlo" select="hardyweinbergGuoThompson[@type='monte-carlo']/genotypeSimulatedStatistic[@statistic='diff_statistic']"/>

     <xsl:variable name="stats-chen-mcmc" select="hardyweinbergGuoThompson[not(@type='monte-carlo')]/genotypeSimulatedStatistic[@statistic='chen_statistic']"/>

     <xsl:variable name="stats-diff-mcmc" select="hardyweinbergGuoThompson[not(@type='monte-carlo')]/genotypeSimulatedStatistic[@statistic='diff_statistic']"/>
     <xsl:variable name="offset" select="count(hardyweinberg/genotypetable/genotype)"/>

     <xsl:for-each select="hardyweinberg/genotypetable/genotype">
      <xsl:variable name="pos" select="position()"/>
      <xsl:variable name="pos-less1" select="position()-1"/>
      <xsl:value-of select="$curr-line-start"/>

      <xsl:value-of select="../../../@name"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:value-of select="@col"/>
      <xsl:text>:</xsl:text>
      <xsl:value-of select="@row"/>
      <xsl:text>&#09;</xsl:text>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="observed"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="expected"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="pvalue"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="chenPvalue"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$pvals-chen-mcmc[$pos]"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$pvals-chen-monte-carlo[$pos]"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$pvals-diff-mcmc[$pos]"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$pvals-diff-monte-carlo[$pos]"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$pvals-diff-enum[$pos]"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$pvals-diff-enum-3x3[$pos]"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$pvals-chen-enum[$pos]"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$pvals-chen-enum-3x3[$pos]"/>
      </xsl:call-template>

      <!-- output steps -->
      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$steps-mcmc"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="$steps-monte-carlo"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node"
       select="../../../hardyweinbergGuoThompson[@type='monte-carlo']/genotypeObservedStatistic[@statistic='chen_statistic' and @id=$pos-less1]"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="../../../hardyweinbergGuoThompson[@type='monte-carlo']/genotypeObservedStatistic[@statistic='diff_statistic' and @id=$pos-less1]"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="../../../hardyweinbergGuoThompson[not(@type='monte-carlo')]/genotypeObservedStatistic[@statistic='chen_statistic' and @id=$pos-less1]"/>
      </xsl:call-template>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="../../../hardyweinbergGuoThompson[not(@type='monte-carlo')]/genotypeObservedStatistic[@statistic='diff_statistic' and @id=$pos-less1]"/>
      </xsl:call-template>

      <xsl:if test="$output.genotype.distrib=1">

       <xsl:variable name="genotype-filename">
	<xsl:text>genotype-</xsl:text>
	<xsl:value-of select="@row"/>
	<xsl:text>-</xsl:text>
	<xsl:value-of select="@col"/>
	<xsl:text>.tsv</xsl:text>
       </xsl:variable>
       
       <exsl:document href="{$genotype-filename}"
	omit-xml-declaration="yes"
	method="text">
	
	<xsl:variable name="cur-chen-mc" select="$stats-chen-monte-carlo[@id=$pos-less1]"/>
	
	<xsl:variable name="cur-diff-mc" select="$stats-diff-monte-carlo[@id=$pos-less1]"/>
	
	<xsl:variable name="cur-chen-mcmc" select="$stats-chen-mcmc[@id=$pos-less1]"/>
	
	<xsl:variable name="cur-diff-mcmc" select="$stats-diff-mcmc[@id=$pos-less1]"/>
	
	<xsl:text>stat.chen.mc</xsl:text>
	<xsl:text>&#09;</xsl:text>
	<xsl:text>stat.diff.mc</xsl:text>
	<xsl:text>&#09;</xsl:text>
	<xsl:text>stat.chen.mcmc</xsl:text>
	<xsl:text>&#09;</xsl:text>
	<xsl:text>stat.diff.mcmc</xsl:text>
	<xsl:call-template name="newline"/>
	
	<xsl:for-each select="$cur-chen-mc">
	 <xsl:variable name="cur-pos" select="position()"/>
	 <xsl:value-of select="."/>
	 <xsl:text>&#09;</xsl:text>
	 <xsl:value-of select="$cur-diff-mc[$cur-pos]"/>
	 <xsl:text>&#09;</xsl:text>
	 <xsl:value-of select="$cur-chen-mcmc[$cur-pos]"/>
	 <xsl:text>&#09;</xsl:text>
	 <xsl:value-of select="$cur-diff-mcmc[$cur-pos]"/>
	 
	 <xsl:call-template name="newline"/>
	</xsl:for-each>
       </exsl:document>
       </xsl:if>

       <xsl:call-template name="newline"/>
     </xsl:for-each>
    </xsl:when>

    <xsl:when test="$type='1-locus-pairwise-fnd'">

     <xsl:call-template name="line-start">
      <xsl:with-param name="popnode" select="../../populationdata" />
     </xsl:call-template>
     
     <!-- make sure locus1 and locus2 are always in map order -->
     <xsl:for-each select="str:tokenize(@locus, ':')">
      <xsl:sort select="$map-order[.=current()]/@order" data-type="number"/>
      <xsl:value-of select="." />
      <xsl:text>&#09;</xsl:text>
     </xsl:for-each>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="@metalocus"/>
     </xsl:call-template>
     
     <xsl:call-template name="output-field">
      <xsl:with-param name="node" select="homozygosityEWSlatkinExact/normDevHomozygosity"/>
     </xsl:call-template>

     <xsl:call-template name="newline"/>
    </xsl:when>

    <xsl:when test="$type='multi-locus-summary'">

     <!-- only attempt to print summary data if haplotype est. converged -->

     <xsl:if test="haplotypefreq/condition/@role='converged'">
      <xsl:call-template name="line-start">
       <xsl:with-param name="popnode" select="../../populationdata" />
      </xsl:call-template>
      
      <xsl:call-template name="output-field">
       <xsl:with-param name="node"
	select="number(individcount[@role='after-filtering']) * 2"/>
      </xsl:call-template>
      
      <!-- make sure locus1 and locus2 are always in map order -->
      <xsl:for-each select="str:tokenize(@loci, ':')">
       <xsl:sort select="$map-order[.=current()]/@order" data-type="number"/>
       <xsl:value-of select="." />
       <xsl:text>&#09;</xsl:text>
      </xsl:for-each>

      <xsl:call-template name="output-field">
       <xsl:with-param name="node" select="@metaloci"/>
      </xsl:call-template>

      <xsl:if test="$pairwise=1">
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="linkagediseq/summary/dprime"/>
       </xsl:call-template>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="linkagediseq/summary/wn"/>
       </xsl:call-template>

       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="linkagediseq/summary/ALD_1_2"/>
       </xsl:call-template>

       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="linkagediseq/summary/ALD_2_1"/>
       </xsl:call-template>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="linkagediseq/summary/q/chisq"/>
       </xsl:call-template>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="linkagediseq/summary/q/dof"/>
       </xsl:call-template>     
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="permutationSummary/pvalue"/>
       </xsl:call-template>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="permutationSummary/lr"/>
       </xsl:call-template>
       
      </xsl:if>
      
      <xsl:call-template name="newline"/>
      
     </xsl:if>
     
    </xsl:when>
    
    <xsl:when test="$type='multi-locus-haplo'">

     <!-- print out message if haplotype estimation failed to converge -->
     <xsl:message>
      <xsl:if test="contains(haplotypefreq/loginfo, 'Percent of iterations with error_flag = 0:   0.000')">
       <xsl:text>Problem with convergence of haplotype </xsl:text>
       <xsl:value-of select="@loci"/> 
       <xsl:text> in file: </xsl:text>
       <xsl:value-of select="../../filename"/>
       <xsl:call-template name="newline"/>
       <xsl:value-of select="substring-before(haplotypefreq/loginfo, '--- Codes for error_flag')"/>
      </xsl:if>
     </xsl:message>

     <!-- only attempt to print haplotypes if converged -->
     <xsl:if test="haplotypefreq/condition/@role='converged'">
     
      <xsl:variable name="curr-line-start">
       <xsl:call-template name="line-start">
	<xsl:with-param name="popnode" select="../../populationdata"/>
       </xsl:call-template>

       <!-- make sure locus1 and locus2 are always in map order -->
       <xsl:for-each select="str:tokenize(@loci, ':')">
	<xsl:sort select="$map-order[.=current()]/@order" data-type="number"/>
	<xsl:value-of select="." />
	<xsl:if test="position()!=last()">
	 <xsl:text>:</xsl:text>
	</xsl:if>
       </xsl:for-each>
       
       <xsl:text>&#09;</xsl:text>
       
      </xsl:variable>
      
      
      <xsl:for-each select="haplotypefreq/haplotype">
       
       <xsl:value-of select="$curr-line-start"/>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="@name"/>
       </xsl:call-template>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="frequency"/>
       </xsl:call-template>
       
       <xsl:call-template name="output-field">
	<xsl:with-param name="node" select="numCopies"/>
       </xsl:call-template>
       
       <xsl:if test="$pairwise=1">
	
	<xsl:variable name="first">
	 <xsl:value-of select="substring-before(@name, '~')"/>	  
	</xsl:variable>
	<xsl:variable name="second">
	  <xsl:value-of select="substring-after(@name, '~')"/>
	</xsl:variable>
       
	<xsl:variable name="pair"
	 select="../../linkagediseq/loci[1]/allelepair[@first=$first and
	 @second=$second]"/>
	
	<xsl:call-template name="output-field">
	 <xsl:with-param name="node" select="$pair/diseq"/>
	</xsl:call-template>
  	
	<xsl:call-template name="output-field">
	 <xsl:with-param name="node" select="$pair/norm_dij"/>
	</xsl:call-template>
  	
  	<xsl:call-template name="output-field">
	 <xsl:with-param name="node" select="$pair/chisq"/>
	</xsl:call-template>

        <!-- not neeeded: repeats the existing 'haplotype.count' and
             'haplotype.freq' columns

        <xsl:call-template name="output-field">
          <xsl:with-param name="node" select="$pair/observed"/>
        </xsl:call-template>

        <xsl:call-template name="output-field">
          <xsl:with-param name="node" select="frequency"/>
        </xsl:call-template>
	-->
	
        <xsl:call-template name="output-field">
          <xsl:with-param name="node" select="$pair/expected"/>
        </xsl:call-template>

       </xsl:if>

       <xsl:call-template name="newline"/>
       
      </xsl:for-each>

     </xsl:if>

    </xsl:when>

   </xsl:choose>
   
  </xsl:for-each>
 </xsl:template>

 <xsl:template match="/">


  <xsl:choose>

   <xsl:when test="element-available('exsl:document')">

    <xsl:variable name="nodes-1-locus-hardyweinberg" select="/meta/dataanalysis/locus/hardyweinberg | /meta/dataanalysis/locus/hardyweinbergGuoThompson | /meta/dataanalysis/locus/hardyweinbergEnumeration"/>    
    <xsl:if test="count($nodes-1-locus-hardyweinberg) &gt;0">
      <xsl:variable name="outputFile">
	<xsl:value-of select="$filePrefix"/><xsl:text>1-locus-hardyweinberg.tsv</xsl:text>
      </xsl:variable>
      <xsl:value-of select="$outputFile"/><xsl:call-template name="newline"/>  <!-- pass through to stdout -->
      
      <exsl:document href="{$outputFile}" omit-xml-declaration="yes" method="text">
	<xsl:call-template name="header-line-start">
	  <xsl:with-param name="popnode" select="/meta/dataanalysis[1]/populationdata"/>
	</xsl:call-template>
	<xsl:text>locus&#09;lump&#09;k&#09;gt.pval&#09;gt.monte-carlo.pval&#09;hw.enum.pval&#09;hw.chisq.pval&#09;hw.homo.chisq.pval&#09;hw.het.chisq.pval&#09;gt.arl.pval&#09;gt.arl.pval.sd&#09;gt.arl.exp.het&#09;gt.arl.obs.het&#09;n.common.genos&#09;n.common.genos.sig&#09;n.common.heteros&#09;n.common.heteros.sig&#09;</xsl:text>
	<xsl:call-template name="newline"/>
	<xsl:call-template name="gen-lines">
	  <xsl:with-param name="nodes" select="/meta/dataanalysis/locus"/>
	  <xsl:with-param name="type" select="'1-locus-hardyweinberg'"/>
	</xsl:call-template>
      </exsl:document>
    </xsl:if>

    <xsl:variable name="nodes-1-locus-summary" select="/meta/dataanalysis/locus"/>    
    <xsl:if test="count($nodes-1-locus-summary) &gt;0">
      <xsl:variable name="outputFile">
	<xsl:value-of select="$filePrefix"/><xsl:text>1-locus-summary.tsv</xsl:text>
      </xsl:variable>
      <xsl:value-of select="$outputFile"/><xsl:call-template name="newline"/>  <!-- pass through to stdout -->
      
      <exsl:document href="{$outputFile}" omit-xml-declaration="yes" method="text">
	<xsl:call-template name="header-line-start">
	  <xsl:with-param name="popnode" select="/meta/dataanalysis[1]/populationdata"/>
	</xsl:call-template>
	<xsl:text>locus&#09;n.gametes&#09;untyped&#09;unsequenced&#09;k&#09;f.pval.lower&#09;f.pval.upper&#09;fnd.lookup&#09;gt.pval&#09;gt.monte-carlo.pval&#09;hw.enum.pval&#09;hw.chisq.pval&#09;hw.homo.chisq.pval&#09;hw.het.chisq.pval&#09;gt.arl.pval&#09;gt.arl.pval.sd&#09;gt.arl.exp.het&#09;gt.arl.obs.het&#09;f.slatkin.obs&#09;f.slatkin.exp&#09;f.slatkin.fnd&#09;f.slatkin.pval&#09;f.slatkin.var&#09;ewens.pval&#09;n.common.genos&#09;n.common.genos.sig&#09;n.common.heteros&#09;n.common.heteros.sig&#09;</xsl:text>
	<xsl:call-template name="newline"/>
	<xsl:call-template name="gen-lines">
	  <xsl:with-param name="nodes" select="$nodes-1-locus-summary"/>
	  <xsl:with-param name="type" select="'1-locus-summary'"/>
	</xsl:call-template>
      </exsl:document>
    </xsl:if>

    <xsl:variable name="nodes-1-locus-allele" select="/meta/dataanalysis/locus/allelecounts/allele"/>    
    <xsl:if test="count($nodes-1-locus-allele) &gt;0">

      <xsl:variable name="outputFile">
	<xsl:value-of select="$filePrefix"/><xsl:text>1-locus-allele.tsv</xsl:text>
      </xsl:variable>

      <xsl:value-of select="$outputFile"/><xsl:call-template name="newline"/>  <!-- pass through to stdout -->
      
      <exsl:document href="{$outputFile}" omit-xml-declaration="yes" method="text">
	<xsl:call-template name="header-line-start">
	  <xsl:with-param name="popnode" select="/meta/dataanalysis[1]/populationdata"/>
	</xsl:call-template>
	<xsl:text>locus&#09;allele&#09;allele.freq&#09;allele.count</xsl:text>
	<xsl:call-template name="newline"/>
	<xsl:call-template name="gen-lines">
	  <xsl:with-param name="nodes" select="/meta/dataanalysis/locus"/>
	  <xsl:with-param name="type" select="'1-locus-allele'"/>
	</xsl:call-template>
      </exsl:document>
    </xsl:if>

    <xsl:variable name="nodes-1-locus-genotype" select="/meta/dataanalysis/locus/hardyweinberg/genotypetable/genotype"/>    
    <xsl:if test="count($nodes-1-locus-genotype) &gt;0">
      
      <xsl:variable name="outputFile">
	<xsl:value-of select="$filePrefix"/><xsl:text>1-locus-genotype.tsv</xsl:text>
      </xsl:variable>
      <xsl:value-of select="$outputFile"/><xsl:call-template name="newline"/>  <!-- pass through to stdout -->
      
      <exsl:document href="{$outputFile}" omit-xml-declaration="yes" method="text">
	<xsl:call-template name="header-line-start">
	  <xsl:with-param name="popnode" select="/meta/dataanalysis[1]/populationdata"/>
	</xsl:call-template>
	<xsl:text>locus&#09;genotype&#09;observed&#09;expected&#09;pval.chisq&#09;pval.chisq.chen&#09;pval.chen.mcmc&#09;pval.chen.monte-carlo&#09;pval.diff.mcmc&#09;pval.diff.monte-carlo&#09;pval.diff.enum&#09;pval.diff.enum.three&#09;pval.chen.enum&#09;pval.chen.enum.three&#09;steps.mcmc&#09;steps.monte.carlo&#09;stat.chen.mc&#09;stat.diff.mc&#09;stat.chen.mcmc&#09;stat.diff.mcmc</xsl:text>
	
	<xsl:call-template name="newline"/>
	<xsl:call-template name="gen-lines">
	  <xsl:with-param name="nodes" select="/meta/dataanalysis/locus"/>
	  <xsl:with-param name="type" select="'1-locus-genotype'"/>
	</xsl:call-template>
      </exsl:document>
    </xsl:if>

    <xsl:variable name="nodes-1-locus-pairwise-fnd" select="/meta/dataanalysis/homozygosityEWSlatkinExactPairwise/group"/>    
    <xsl:if test="count($nodes-1-locus-pairwise-fnd) &gt;0">
      <xsl:variable name="outputFile">
	<xsl:value-of select="$filePrefix"/><xsl:text>1-locus-pairwise-fnd.tsv</xsl:text>
      </xsl:variable>
      <xsl:value-of select="$outputFile"/><xsl:call-template name="newline"/>  <!-- pass through to stdout -->

      <exsl:document href="{$outputFile}" omit-xml-declaration="yes" method="text">
	<xsl:call-template name="header-line-start">
	  <xsl:with-param name="popnode" select="/meta/dataanalysis[1]/populationdata"/>
	</xsl:call-template>
	<xsl:text>locus1&#09;locus2&#09;metaloci&#09;f.slatkin.fnd</xsl:text>
	<xsl:call-template name="newline"/>
	
	<xsl:call-template name="gen-lines">
	  <xsl:with-param name="nodes" select="$nodes-1-locus-pairwise-fnd"/>
	  <xsl:with-param name="type" select="'1-locus-pairwise-fnd'"/>
	</xsl:call-template>
      </exsl:document>
    </xsl:if>

    <xsl:variable name="nodes-2-locus" select="/meta/dataanalysis/emhaplofreq/group[(@mode='all-pairwise-ld-with-permu' or @mode='all-pairwise-ld-no-permu' or (@mode='haplo' and (string-length(@loci) - string-length(translate(@loci, ':', '')))=1)) and not(@role='no-data')]"/>
    <xsl:if test="count($nodes-2-locus) &gt;0">
      <xsl:variable name="outputFile">
	<xsl:value-of select="$filePrefix"/><xsl:text>2-locus-summary.tsv</xsl:text>
      </xsl:variable>
      <xsl:value-of select="$outputFile"/><xsl:call-template name="newline"/>  <!-- pass through to stdout -->

      <exsl:document href="{$outputFile}" omit-xml-declaration="yes" method="text">
	<xsl:call-template name="header-line-start">
	  <xsl:with-param name="popnode" select="/meta/dataanalysis[1]/populationdata"/>
	</xsl:call-template>
	<xsl:text>n.gametes&#09;locus1&#09;locus2&#09;metaloci&#09;ld.dprime&#09;ld.wn&#09;ald.1_2&#09;ald.2_1&#09;q.chisq&#09;q.df&#09;lrt.pval&#09;lrt.z</xsl:text>
	<xsl:call-template name="newline"/>
	<xsl:call-template name="gen-lines">
	  <!-- either explicitly set as an all-pairwise mode, or 'haplo' mode with 2 loci -->
	  <xsl:with-param name="nodes" select="$nodes-2-locus"/>
	  <xsl:with-param name="type" select="'multi-locus-summary'"/>
	</xsl:call-template>
      </exsl:document>

      <xsl:variable name="outputFile2">
	<xsl:value-of select="$filePrefix"/><xsl:text>2-locus-haplo.tsv</xsl:text>
      </xsl:variable>
      <xsl:value-of select="$outputFile2"/><xsl:call-template name="newline"/> <!-- pass through to stdout -->

      <exsl:document href="{$outputFile2}" omit-xml-declaration="yes" method="text">
	<xsl:call-template name="header-line-start">
	  <xsl:with-param name="popnode" select="/meta/dataanalysis[1]/populationdata"/>
	</xsl:call-template>
	<xsl:text>loci&#09;haplotype&#09;haplotype.freq&#09;haplotype.count&#09;ld.d&#09;ld.dprime&#09;ld.chisq&#09;haplotype.no-ld.count</xsl:text>
	<xsl:call-template name="newline"/>
	<xsl:call-template name="gen-lines">
	  <!-- either explicitly set as an all-pairwise mode, or 'haplo' mode with 2 loci -->
	  <xsl:with-param name="nodes" select="$nodes-2-locus"/>
	  <xsl:with-param name="type" select="'multi-locus-haplo'"/>
	</xsl:call-template>
      </exsl:document>
    </xsl:if>

    <!-- deal with all output groups WITH 3 OR MORE LOCI -->
    
    <xsl:variable name="nodes-3-or-greater-loci" select="/meta/dataanalysis/emhaplofreq/group[not(@role='no-data')]"/>
    <xsl:variable name="popnode" select="/meta/dataanalysis[1]/populationdata"/>
    
    <xsl:variable name="loci-counts">
      <xsl:for-each select="$nodes-3-or-greater-loci/@loci">
	<locus_count><xsl:value-of select="string-length(.) - string-length(translate(., ':', '')) + 1"/></locus_count>
      </xsl:for-each>
    </xsl:variable>

    <!-- get unique haplotype lengths across all output -->
    <!-- dynamically generate files, rather than hardcoding -->
    <xsl:variable name="unique-loci-counts" select="set:distinct(exsl:node-set($loci-counts)/locus_count)"/>
    
    <xsl:for-each select="$unique-loci-counts">
      <xsl:variable name="loci_count" select="."/>

      <xsl:if test="$loci_count &gt; 2">  <!-- only for 3 haplotypes or longer -->

	<xsl:variable name="outputFile">
	  <xsl:value-of select="$filePrefix"/><xsl:value-of select="$loci_count"/><xsl:text>-locus-summary.tsv</xsl:text>
	</xsl:variable>
	<xsl:value-of select="$outputFile"/><xsl:call-template name="newline"/>  <!-- pass through to stdout -->
	
	<exsl:document href="{$outputFile}" omit-xml-declaration="yes" method="text">
	  <xsl:call-template name="header-line-start">
	    <xsl:with-param name="popnode" select="$popnode"/>
	  </xsl:call-template>
	  <xsl:text>n.gametes&#09;</xsl:text>
	  <!-- dynamically generate headers -->
	  <xsl:call-template name="generate-n-headers">  
	    <xsl:with-param name="i" select="1"/>
	    <xsl:with-param name="max" select="$loci_count"/>
	    <xsl:with-param name="prefix" select="'locus'"/>
	    <xsl:with-param name="suffix" select="'&#09;'"/>      
	  </xsl:call-template>
	  <xsl:text>metaloci</xsl:text>	
	  
	  <xsl:call-template name="newline"/>
	  <xsl:call-template name="gen-lines">
	    <xsl:with-param name="nodes"
			    select="$nodes-3-or-greater-loci[(string-length(@loci) - string-length(translate(@loci, ':', '')) + 1)=$loci_count]"/>
	    <xsl:with-param name="type" select="'multi-locus-summary'"/>
	    <xsl:with-param name="pairwise" select="0"/>
	  </xsl:call-template>
	</exsl:document>

	<xsl:variable name="outputFile2">
	  <xsl:value-of select="$filePrefix"/><xsl:value-of select="$loci_count"/><xsl:text>-locus-haplo.tsv</xsl:text>
	</xsl:variable>
	<xsl:value-of select="$outputFile2"/><xsl:call-template name="newline"/>  <!-- pass through to stdout -->
	
	<exsl:document href="{$outputFile2}" omit-xml-declaration="yes" method="text">
	  <xsl:call-template name="header-line-start">
	    <xsl:with-param name="popnode" select="$popnode"/>
	  </xsl:call-template>
	  <xsl:text>loci&#09;haplotype&#09;haplotype.freq&#09;haplotype.count</xsl:text>
	  <xsl:call-template name="newline"/>
	  <xsl:call-template name="gen-lines">
	    <xsl:with-param name="nodes" select="$nodes-3-or-greater-loci[(string-length(@loci) - string-length(translate(@loci, ':', '')) + 1)=$loci_count]"/>
	    <xsl:with-param name="type" select="'multi-locus-haplo'"/>
	    <xsl:with-param name="pairwise" select="0"/>
	  </xsl:call-template>
	</exsl:document>
	
      </xsl:if>
    </xsl:for-each>

    </xsl:when>

   <xsl:otherwise>
    <xsl:message>needs a processor that understands exsl elements, see http://exsl.org/
    </xsl:message>
   </xsl:otherwise>
  </xsl:choose>

 </xsl:template>

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
